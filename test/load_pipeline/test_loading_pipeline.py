import gc
import os
import shutil
import time
from typing import List, Tuple, Dict, Set

import duckdb
import h3
import pytest
from pandas import DataFrame

from common import const
from loader.aggregation_step import MinAggregation, MaxAggregation
from loader.load_pipeline import LoadingPipeline
from loader.output_step import LocalDuckdbOutputStep
from loader.postprocessing_step import MultiplyValue
from loader.preprocessing_step import PreprocessingStep
from loader.reading_step import ParquetFileReader

data_dir = "./test/test_data/loading_pipeline/"

tmp_folder = f"{data_dir}/tmp"


@pytest.fixture()
def database_dir():
    if os.path.exists(tmp_folder):
        shutil.rmtree(tmp_folder)
    os.mkdir(tmp_folder)

    yield tmp_folder

    # gc + delay is necessary as without manual call tests may complete
    #  before db instances are cleaned up. This causes a file lock to persist
    #  that prevents cleanup of the temp directory.
    gc.collect()
    time.sleep(0.1)
    if os.path.exists(tmp_folder):
        shutil.rmtree(tmp_folder)


def read_temp_db(dataset_name: str) -> List[Tuple]:
    db_path = f"{tmp_folder}/{dataset_name}.duckdb"
    table = f"{dataset_name}"
    connection = duckdb.connect(db_path)

    out = connection.execute(
        f"select * from {table}"
    ).fetchall()

    return out


def read_metadata_db(dataset_name: str) -> List[Tuple]:
    db_path = f"{tmp_folder}/dataset_metadata.duckdb"
    table = f"dataset_metadata"
    connection = duckdb.connect(db_path)

    out = connection.execute(
        f"select * from {table} where dataset_name = '{dataset_name}'"
    ).fetchall()

    return out


class AddOnePre(PreprocessingStep):

    def __init__(self, conf_dict: Dict[str, str]):
        pass

    def run(self, input_df: DataFrame) -> DataFrame:
        for col in input_df:
            if col == 'latitude' or col == 'longitude':
                continue
            input_df[col] = input_df[col] + 1
        return input_df

def round_floats(input: Set[Tuple]) -> Set[Tuple]:
    # database seems to result in floating point errors in some tests
    # ex. 50.1 -> 50.999956 or something
    # this corrects by rounding to actual accuracy
    out = set()
    for tpl in input:
        new_l = []
        for v in tpl:
            if isinstance(v, float):
                new_l.append(round(v,1))
            else:
                new_l.append(v)
        out.add(tuple(new_l))
    return out

class TestLoadingPipeline:

    def test_read_out_only(self, database_dir):
        parquet_file = data_dir + "/2_cell_agg.parquet"
        dataset = "read_out_only"

        read_step = ParquetFileReader({
            "file_path": parquet_file,
            "data_columns": ["value1", "value2"]
        })

        output_step = LocalDuckdbOutputStep({
            "database_dir": database_dir,
            "dataset_name": dataset,
            "mode": "create"
        })

        pipeline = LoadingPipeline(
            read_step, [], [], [], output_step, 1
        )

        pipeline.run()

        out = read_temp_db(dataset)

        # the same as the raw data in the initial file
        expected = {
            (50, 50, 10, 100),
            (50.1, 50.1, 0, 0),
            (50.2, 50.2, 2, 20),
            (-50, -50, 10, 100),
            (-50.1, -50.1, 0, 0),
            (-50.2, -50.2, 2, 20),
        }

        assert round_floats(set(out)) == expected

    def test_read_out_preprocess(self, database_dir):
        parquet_file = data_dir + "/2_cell_agg.parquet"
        dataset = "read_out_only"

        read_step = ParquetFileReader({
            "file_path": parquet_file,
            "data_columns": ["value1", "value2"]
        })

        output_step = LocalDuckdbOutputStep({
            "database_dir": database_dir,
            "dataset_name": dataset,
            "mode": "create"
        })

        pre_step = AddOnePre({})

        pipeline = LoadingPipeline(
            read_step, [pre_step], [], [], output_step, 1
        )

        pipeline.run()

        out = read_temp_db(dataset)

        # the same as the raw data in the initial file
        expected = {
            (50, 50, 11, 101),
            (50.1, 50.1, 1, 1),
            (50.2, 50.2, 3, 21),
            (-50, -50, 11, 101),
            (-50.1, -50.1, 1, 1),
            (-50.2, -50.2, 3, 21),
        }

        assert round_floats(set(out)) == expected

    def test_read_out_aggregate(self, database_dir):
        parquet_file = data_dir + "/2_cell_agg.parquet"
        dataset = "read_out_only"

        read_step = ParquetFileReader({
            "file_path": parquet_file,
            "data_columns": ["value1", "value2"]
        })

        output_step = LocalDuckdbOutputStep({
            "database_dir": database_dir,
            "dataset_name": dataset,
            "mode": "create"
        })

        agg_steps = [
            MinAggregation({}),
            MaxAggregation({})
        ]

        pipeline = LoadingPipeline(
            read_step, [], agg_steps, [], output_step, 1
        )

        pipeline.run()

        out = read_temp_db(dataset)
        def round_latlong(t:Tuple) -> Tuple:
            as_l = list(t)
            as_l[5] = round(as_l[5], 4)
            as_l[6] = round(as_l[6], 4)
            return tuple(as_l)

        out = list(map(
            round_latlong,
            out
        ))

        # the same as the raw data in the initial file
        cell1_lat, cell1_long = h3.cell_to_latlng('8110bffffffffff')
        cell2_lat, cell2_long = h3.cell_to_latlng('81defffffffffff')
        expected = {
            ('8110bffffffffff', 0, 10, 0, 100,
             cell1_lat, cell1_long),
            ('81defffffffffff', 0, 10, 0, 100,
             cell2_lat, cell2_long),
        }

        assert round_floats(set(out)) == round_floats(expected)

    def test_fail_if_agg_but_no_res(self, database_dir):
        parquet_file = data_dir + "/2_cell_agg.parquet"
        dataset = "read_out_only"

        read_step = ParquetFileReader({
            "file_path": parquet_file,
            "data_columns": ["value1", "value2"]
        })

        output_step = LocalDuckdbOutputStep({
            "database_dir": database_dir,
            "dataset_name": dataset,
            "mode": "create"
        })

        agg_steps = [
            MinAggregation({}),
            MaxAggregation({})
        ]

        with pytest.raises(ValueError):
            LoadingPipeline(
                read_step, [], agg_steps, [], output_step, None
            )

    def test_read_out_post(self, database_dir):
        parquet_file = data_dir + "/2_cell_agg.parquet"
        dataset = "read_out_only"

        read_step = ParquetFileReader({
            "file_path": parquet_file,
            "data_columns": ["value1", "value2"]
        })

        output_step = LocalDuckdbOutputStep({
            "database_dir": database_dir,
            "dataset_name": dataset,
            "mode": "create"
        })

        post_step = MultiplyValue({"multiply_by": 2})

        pipeline = LoadingPipeline(
            read_step, [], [], [post_step], output_step, 1
        )

        pipeline.run()

        out = read_temp_db(dataset)

        # the same as the raw data in the initial file
        expected = {
            (50, 50, 10 * 2, 100 * 2),
            (50.1, 50.1, 0 * 2, 0 * 2),
            (50.2, 50.2, 2 * 2, 20 * 2),
            (-50, -50, 10 * 2, 100 * 2),
            (-50.1, -50.1, 0 * 2, 0 * 2),
            (-50.2, -50.2, 2 * 2, 20 * 2),
        }

        assert round_floats(set(out)) == expected

    def test_full_pipeline(self, database_dir):
        parquet_file = data_dir + "/2_cell_agg.parquet"
        dataset = "full_pipeline"

        read_step = ParquetFileReader({
            "file_path": parquet_file,
            "data_columns": ["value1", "value2"]
        })

        output_step = LocalDuckdbOutputStep({
            "database_dir": database_dir,
            "dataset_name": dataset,
            "mode": "create"
        })

        pre_step = AddOnePre({})

        agg_steps = [
            MinAggregation({}),
            MaxAggregation({})
        ]
        post_step = MultiplyValue({"multiply_by": 2})

        pipeline = LoadingPipeline(
            read_step, [pre_step], agg_steps, [post_step], output_step, 1
        )

        pipeline.run()

        out = read_temp_db(dataset)

        cell1_lat, cell1_long = h3.cell_to_latlng('8110bffffffffff')
        cell2_lat, cell2_long = h3.cell_to_latlng('81defffffffffff')

        def f(i: int):
            return (i + 1) * 2

        # the same as the raw data in the initial file
        expected = {
            ('8110bffffffffff', f(0), f(10), f(0), f(100),
             cell1_lat, cell1_long),
            ('81defffffffffff', f(0), f(10), f(0), f(100),
             cell2_lat, cell2_long),
        }

        assert round_floats(set(out)) == round_floats(expected)

    def test_additional_key_cols(self, database_dir):
        parquet_file = data_dir + "with_company.parquet"
        dataset = "read_out_only"

        read_step = ParquetFileReader({
            "file_path": parquet_file,
            "data_columns": ["value1", "value2"],
            "key_columns": ["company"]
        })

        output_step = LocalDuckdbOutputStep({
            "database_dir": database_dir,
            "dataset_name": dataset,
            "mode": "create",
            "key_columns": ["company"]
        })

        agg_steps = [
            MinAggregation({}),
            MaxAggregation({})
        ]

        pipeline = LoadingPipeline(
            read_step, [], agg_steps, [], output_step, 1
        )

        pipeline.run()

        out = read_temp_db(dataset)
        def round_latlong(t:Tuple) -> Tuple:
            as_l = list(t)
            as_l[5] = round(as_l[5], 4)
            as_l[6] = round(as_l[6], 4)
            return tuple(as_l)

        out = list(map(
            round_latlong,
            out
        ))

        # the same as the raw data in the initial file
        cell1_lat, cell1_long = h3.cell_to_latlng('8110bffffffffff')
        cell2_lat, cell2_long = h3.cell_to_latlng('81defffffffffff')

        # the same as the raw data in the initial file
        expected = {
            ('company1', '8110bffffffffff', 0, 10, 0, 100,
             cell1_lat, cell1_long),
            ('company2', '8110bffffffffff', 2, 2, 20, 20,
             cell1_lat, cell1_long),
            ('company1', '81defffffffffff', 0, 10, 0, 100,
             cell2_lat, cell2_long),
            ('company2', '81defffffffffff', 2, 2, 20, 20,
             cell2_lat, cell2_long)
        }

        assert round_floats(set(out)) == round_floats(expected)

    def test_metadata_creation(self, database_dir):
        parquet_file = data_dir + "/2_cell_agg.parquet"
        dataset = "test_meta_creation"

        read_step = ParquetFileReader({
            "file_path": parquet_file,
            "data_columns": ["value1", "value2"],
        })

        output_step = LocalDuckdbOutputStep({
            "database_dir": database_dir,
            "dataset_name": dataset,
            "mode": "create",
            "description": "A Test Dataset",
            "dataset_type": "point",
            "key_columns": ["latitude", "longitude"]
        })

        pipeline = LoadingPipeline(
            read_step, [], [], [], output_step, 1
        )

        pipeline.run()

        out = read_metadata_db(dataset)

        expected = [(
            dataset,
            "A Test Dataset",
            {"key": ["latitude", "longitude"], "value": ["REAL", "REAL"]},
            {"key": ["value1", "value2"], "value": ["INTEGER", "INTEGER"]},
            "point"
        )]
        assert out == expected
