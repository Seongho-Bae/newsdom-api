import json
from pathlib import Path
from unittest.mock import patch

import pytest

from tools.export_jsonl import export_jsonl, main


def test_export_jsonl_valid(tmp_path: Path):
    input_file = tmp_path / "input.json"
    data = {
        "document_id": "doc_1",
        "pages": [
            {
                "page_number": "1",
                "articles": [
                    {
                        "article_id": "art_1",
                        "headline": "Headline 1",
                        "body_blocks": ["Block 1", "Block 2"],
                    },
                    {
                        "article_id": "art_2",
                        "headline": "Headline 2",
                        "body_blocks": [],
                    },
                ],
            },
            "invalid_page_type",
        ],
    }
    input_file.write_text(json.dumps(data), encoding="utf-8")

    output_file = tmp_path / "output.jsonl"
    export_jsonl(input_file, output_file)

    lines = output_file.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 3

    records = [json.loads(line) for line in lines]
    assert records[0] == {
        "document_id": "doc_1",
        "page_number": "1",
        "article_id": "art_1",
        "headline": "Headline 1",
        "body_block_index": 0,
        "body_block_text": "Block 1",
    }
    assert records[1] == {
        "document_id": "doc_1",
        "page_number": "1",
        "article_id": "art_1",
        "headline": "Headline 1",
        "body_block_index": 1,
        "body_block_text": "Block 2",
    }
    assert records[2] == {
        "document_id": "doc_1",
        "page_number": "1",
        "article_id": "art_2",
        "headline": "Headline 2",
        "body_block_index": "",
        "body_block_text": "",
    }


def test_export_jsonl_invalid_article_type(tmp_path: Path):
    input_file = tmp_path / "input.json"
    data = {
        "document_id": "doc_1",
        "pages": [
            {
                "page_number": "1",
                "articles": [
                    "invalid_article_type",
                    {
                        "article_id": "art_1",
                        "headline": "Headline 1",
                        "body_blocks": ["Block 1"],
                    },
                ],
            }
        ],
    }
    input_file.write_text(json.dumps(data), encoding="utf-8")

    output_file = tmp_path / "output.jsonl"
    export_jsonl(input_file, output_file)

    lines = output_file.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 1

    record = json.loads(lines[0])
    assert record == {
        "document_id": "doc_1",
        "page_number": "1",
        "article_id": "art_1",
        "headline": "Headline 1",
        "body_block_index": 0,
        "body_block_text": "Block 1",
    }


def test_export_jsonl_not_found():
    with pytest.raises(FileNotFoundError):
        export_jsonl(Path("non_existent.json"), Path("output.jsonl"))


def test_export_jsonl_wrong_extension(tmp_path: Path):
    input_file = tmp_path / "input.txt"
    input_file.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="must be a .json file"):
        export_jsonl(input_file, tmp_path / "output.jsonl")


def test_export_jsonl_invalid_json(tmp_path: Path):
    input_file = tmp_path / "input.json"
    input_file.write_text("invalid json", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid JSON file"):
        export_jsonl(input_file, tmp_path / "output.jsonl")


def test_export_jsonl_preserves_published_output_when_encoding_fails(tmp_path: Path):
    input_file = tmp_path / "input.json"
    data = {
        "document_id": "doc_1",
        "pages": [
            {
                "page_number": "1",
                "articles": [
                    {
                        "article_id": "art_1",
                        "headline": "Headline 1",
                        "body_blocks": ["Block 1"],
                    }
                ],
            }
        ],
    }
    input_file.write_text(json.dumps(data), encoding="utf-8")

    output_file = tmp_path / "output.jsonl"
    output_file.write_text("existing content", encoding="utf-8")

    with patch("json.dumps", side_effect=Exception("Encoding error")):
        with pytest.raises(Exception, match="Encoding error"):
            export_jsonl(input_file, output_file)

    assert output_file.read_text(encoding="utf-8") == "existing content"


def test_main_success(tmp_path: Path, capsys):
    input_file = tmp_path / "input.json"
    input_file.write_text("{}", encoding="utf-8")
    output_file = tmp_path / "output.jsonl"

    main([str(input_file), str(output_file)])

    captured = capsys.readouterr()
    assert "JSONL successfully written to" in captured.out


def test_main_error(tmp_path: Path, capsys):
    input_file = tmp_path / "input.json"
    input_file.write_text("invalid json", encoding="utf-8")
    output_file = tmp_path / "output.jsonl"

    with pytest.raises(SystemExit) as excinfo:
        main([str(input_file), str(output_file)])

    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "Error exporting JSONL" in captured.err
