import subprocess
import pickle
import os
import pandas as pd

path = os.path.dirname(__file__)
path_repo_clone = os.path.join(path, 'repoClone.py')
path_stats = os.path.join(path, 'stats')
path_repos = os.path.join(path, 'repos')

csv1_path = f"{path_stats}/github_data.csv"
csv2_path = f"{path_stats}/metricas_repo.csv"
output_csv_path = f"{path_stats}/metricas_repo_combined.csv"  

def clone_repo(repo):
    try:
        os.chdir(path)

        command_clone = f"python {path_repo_clone} {repo}"

        os.system(command_clone)

        # obter métricas do CK
        command_ck = f"java -jar ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar {path_repos} {path_stats}"
        os.system(command_ck)

    except Exception as e:
        print(f"Erro: {e}")

def generate_csv():
    csv_path = "stats/class.csv"
    df = pd.read_csv(csv_path, comment='#')
    
    total_lcom = df["lcom"].sum()
    total_loc = df["loc"].sum()
    total_cbo = df["cbo"].sum()
    total_dit = df["dit"].sum()
    
    totals_df = pd.DataFrame({
        "LCOM": [total_lcom],
        "LOC": [total_loc],
        "CBO": [total_cbo],
        "DIT": [total_dit]
    })
    
    new_csv = "stats/metricas_repo.csv"
    totals_df.to_csv(new_csv, index=False)

def make_full_cv(csv1_path, csv2_path, output_csv_path):
    df1 = pd.read_csv(csv1_path)
    df2 = pd.read_csv(csv2_path)
    
    result_df = pd.concat([df1, df2], ignore_index=True)
    
    result_df.to_csv(output_csv_path, index=False)

if __name__ == "__main__":
    with open('dump.py', 'rb') as arc:
        repos = pickle.load(arc)

    clone_repo(repos[0])
    generate_csv()
    make_full_cv(csv1_path, csv2_path, output_csv_path)  