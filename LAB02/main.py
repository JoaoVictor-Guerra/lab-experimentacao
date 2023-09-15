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
            os.system(f"rd /s /q {path_repos}")



def generate_csv():
    csv_path = "stats/class.csv"
    df = pd.read_csv(csv_path, comment='#')
    
    total_lcom = df["lcom"].median()
    total_loc = df["loc"].sum()
    total_cbo = df["cbo"].median()
    total_dit = df["dit"].max()
    
    new_csv = "stats/metricas_repo.csv"
    
    if os.path.isfile(new_csv):
        existing_df = pd.read_csv(new_csv)
        new_row = pd.DataFrame({
            "LCOM": [total_lcom],
            "LOC": [total_loc],
            "CBO": [total_cbo],
            "DIT": [total_dit]
        })
        updated_df = pd.concat([existing_df, new_row], ignore_index=True)
        
    else:
        updated_df = pd.DataFrame({
            "LCOM": [total_lcom],
            "LOC": [total_loc],
            "CBO": [total_cbo],
            "DIT": [total_dit]
        })
    
    updated_df.to_csv(new_csv, index=False)

def make_full_csv(csv_git_path, csv_ck_path, output_csv_path):
    df1 = pd.read_csv(csv_git_path)
    df2 = pd.read_csv(csv_ck_path)
    
    # Redefina os índices do df2
    df2.reset_index(drop=True, inplace=True)
    
    # Concatene os DataFrames ao longo das linhas
    result_df = pd.concat([df1, df2], axis=1, ignore_index=False)
    
    #print(result_df)

    result_df.to_csv(output_csv_path, index=False)

if __name__ == "__main__":
    with open('LAB02/dump.py', 'rb') as arc:
        repos_total = pickle.load(arc)

        list_repos = pd.read_csv(csv_git_path)
        repos_calculados = pd.read_csv(csv_ck_path)

        print(f'tamanho:{repos_calculados.size}')
        print(f'tamanho/4:{repos_calculados.size/4}')
        i=0
        for index, row in list_repos.iterrows():

            print(index)

            if i >= repos_calculados.size/4:

                clone_repo(repos_total[index])
                generate_csv()  
                dump_repo()
            
            i = i+1 
            print(f'i:{i}')

        make_full_csv(csv_git_path, csv_ck_path, output_csv_path)
                