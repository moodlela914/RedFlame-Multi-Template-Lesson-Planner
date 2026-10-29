"""Both Word templates; legacy Markdown remains digital-ai only."""
import argparse
import json
from pathlib import Path
import re
import sys
import tempfile
from lesson_templates import PROFILES, convert_json

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, 'reconfigure'):
        stream.reconfigure(encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='?', type=Path)
    parser.add_argument('output', nargs='?', type=Path)
    parser.add_argument('--template', choices=tuple(PROFILES))
    parser.add_argument('--list-templates', action='store_true')
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    try:
        if args.list_templates:
            for key, value in PROFILES.items():
                print(f'{key}: {value["name"]}')
            return 0
        if not args.input:
            parser.error('需要輸入 JSON 或舊版 Markdown 檔案')
        source = args.input.resolve()
        output = (args.output or source.with_suffix('.docx')).resolve()
        if source.suffix.lower() == '.json':
            payload = json.loads(source.read_text(encoding='utf-8-sig'))
            convert_json(payload, output, args.template, source, args.check_only)
        elif source.suffix.lower() == '.md':
            if args.template not in (None, 'digital-ai'):
                raise ValueError('跨域格式使用 JSON，請依 references/content-contract.md 生成資料')
            if args.check_only:
                raise ValueError('--check-only 僅支援 JSON')
            if output.exists():
                raise ValueError('輸出檔已存在，請使用新的檔名')
            if output.suffix.lower() != '.docx':
                raise ValueError('輸出副檔名必須為 .docx')
            text = source.read_text(encoding='utf-8-sig')
            if re.search(r'第\s*(?:[4-9]|\d{2,}|[四五六七八九十]+)\s*節', text):
                raise ValueError('舊 Markdown 最多三節；四節以上使用 JSON，避免遺漏內容')
            from legacy_markdown import run_conversion
            output.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.TemporaryDirectory(prefix='lesson-', dir=output.parent) as temp:
                staged = Path(temp) / 'validated.docx'
                if not run_conversion(str(source), str(staged)):
                    raise ValueError('舊 Markdown 檢核未通過，未產生正式輸出')
                with output.open('xb') as target:
                    target.write(staged.read_bytes())
        else:
            raise ValueError('輸入副檔名必須為 .json 或 .md')
        print('資料與範本檢核通過' if args.check_only else f'已產生：{output}')
        return 0
    except (ValueError, OSError, KeyError, TypeError, IndexError) as error:
        print(f'錯誤：{error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
