import pickle
import os
import pandas as pd


path = os.path.dirname(__file__)
path_repo_clone = os.path.join(path, 'repoClone.py')
path_stats = os.path.join(path, 'stats')
path_repos = os.path.join(path, 'repos')

csv_git_path = f"{path_stats}/github_data.csv"
csv_ck_path = f"{path_stats}/metricas_repo.csv"
output_csv_path = f"{path_stats}/metricas_repo_combined.csv"  

def clone_repo(repo):
    try:
        os.chdir(path)

        os.system("mkdir repos")

        command_clone = f"python {path_repo_clone} {repo}"

        os.system(command_clone)

        # obter métricas do CK
        os.chdir(path_stats)

        command_ck = f"java -jar ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar {path_repos} {path_stats}"
        os.system(command_ck)

        os.chdir(path)

    except Exception as e:
        print(f"Erro: {e}")

def dump_repo():
    for root, dirs, files in os.walk(path_repos):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            os.system(f"rd /s /q {path_repos}")#shutil.rmtree(os.path.join(root, d))# "rd /s /q caminho"



def generate_csv():
    csv_path = "stats/class.csv"
    df = pd.read_csv(csv_path, comment='#')
    
    total_lcom = df["lcom"].median()
    total_loc = df["loc"].sum()
    total_cbo = df["cbo"].median()
    total_dit = df["dit"].max()
    
    totals_df = pd.DataFrame({
        "LCOM": [total_lcom],
        "LOC": [total_loc],
        "CBO": [total_cbo],
        "DIT": [total_dit]
    })
    
    new_csv = "stats/metricas_repo.csv"
    totals_df.to_csv(new_csv, index=False)

def make_full_cv(csv_git_path, csv_ck_path, output_csv_path):
    df1 = pd.read_csv(csv_git_path)
    df2 = pd.read_csv(csv_ck_path)
    
    result_df = pd.concat([df1, df2], ignore_index=True)
    
    print(result_df)

    result_df.to_csv(output_csv_path, index=False)

if __name__ == "__main__":
    with open('LAB02/dump.py', 'rb') as arc:
        repos = pickle.load(arc)

    clone_repo(repos[0])
    generate_csv()
    make_full_cv(csv_git_path, csv_ck_path, output_csv_path)  
    dump_repo()