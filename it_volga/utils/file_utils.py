import os
import pandas as pd

def create_task_file(data_dir):
    """Create task file if it doesn't exist."""
    task_file = os.path.join(data_dir, "volgait2024-semifinal-task.csv")
    if not os.path.exists(task_file):
        # Create a dummy task file for testing purposes
        data = {
            'shutdown_id': [1, 2, 3],
            'comment': [
                'из п/з Д=100, без ХВС К. Либкнехта 21, 23, 23а 25',
                'пожар на улице Ленина 15',
                'отключение на 5 дней в районе улицы Гагарина'
            ]
        }
        df = pd.DataFrame(data)
        df.to_csv(task_file, sep=";", index=False, encoding="utf-8")

def save_results(data_dir, results):
    """Save results to a CSV file."""
    result_file = os.path.join(data_dir, "volgait2024-semifinal-result.csv")
    df = pd.DataFrame(results)
    df.to_csv(result_file, sep=";", index=False, encoding="utf-8")