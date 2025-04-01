import pandas as pd
import json
import csv
import os
from typing import Optional, BinaryIO
import io

def load_file(file: BinaryIO) -> Optional[pd.DataFrame]:
    try:
        file_extension = os.path.splitext(file.name)[1].lower()
        file_content = file.read()

        if file_extension == '.csv':

            content = file_content.decode('utf-8')

            if ',' in content[:1000]:
                delimiter = ','
            elif ';' in content[:1000]:
                delimiter = ';'
            elif '\t' in content[:1000]:
                delimiter = '\t'
            else:
                delimiter = ','

            return pd.read_csv(io.StringIO(content), delimiter=delimiter, on_bad_lines='skip')

        elif file_extension == '.json':
            content = file_content.decode('utf-8')
            try:

                data = json.loads(content)
                if isinstance(data, list):
                    return pd.DataFrame(data)
                elif isinstance(data, dict):
                    return pd.DataFrame([data])
                else:
                    return None
            except json.JSONDecodeError:

                lines = content.strip().split('\n')
                data = []
                for line in lines:
                    try:
                        data.append(json.loads(line))
                    except:
                        continue
                return pd.DataFrame(data) if data else None

        elif file_extension == '.txt':

            content = file_content.decode('utf-8')
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            return pd.DataFrame({'text': lines})

        else:

            return None

    except Exception as e:
        print(f"Dosya okuma hatası: {e}")
        return None


def save_processed_data(df: pd.DataFrame, output_format: str = 'csv', output_path: Optional[str] = None) -> str:
    if output_format == 'csv':
        if output_path:
            df.to_csv(output_path, index=False)
            return output_path
        else:
            return df.to_csv(index=False)
    elif output_format == 'json':
        if output_path:
            df.to_json(output_path, orient='records', indent=2)
            return output_path
        else:
            return df.to_json(orient='records', indent=2)
    else:

        if output_path:
            df.to_csv(output_path, index=False)
            return output_path
        else:
            return df.to_csv(index=False)