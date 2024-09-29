import argparse
from src.eval_metric import eval_metric, score_all_free
from src.score import scorer
import pandas as pd
from statistics import mean

parser = argparse.ArgumentParser()
parser.add_argument(
    "--model_type",
    type=str,
    default="",
    help="pretrained model type or path to pretrained model",
)
parser.add_argument("--batch_size", type=int, default=16)
parser.add_argument("--dataset_name", type=str, default=0, help="dataset name")
parser.add_argument("--data_dir", type=str, help="data dir")
parser.add_argument(
    "--setting", type=str, default="need", help="reference needed or free"
)
parser.add_argument("--alpha", type=float, default="0.2", help="alpha in ibleu")
parser.add_argument("--beta", type=float, default="3", help="beta in selfibleu")
parser.add_argument("--extend", type=bool, default=False, help="extended version")
args = parser.parse_args()

def calculate_scores(query: list, hyp: list) -> dict:
    results = {}
    for i in available_metrics:
        try:
            args.metric = i
            out = score_all_free(args, query, hyp)
            results[i] = out
        except:
            print("could not calculate", i)

    average = {}
    for k,v in results.items():
        average[k] = mean(v)
    return average
if __name__ == "__main__":
    available_metrics = [
        # "bleu",
        # "meteor",
        "rougeL",
        "rouge1",
        "rouge2",
        "selfibleu",
        "parascore",
        #"bartscore",
    ]

    data = pd.read_csv("data.csv", sep=",")
    sources = data["source"].tolist()
    hallucinations = data.apply(lambda row: row[row["label"]], axis=1).tolist()
    good_paraphrases = data.apply(lambda row: row["hyp1" if row["label"] == "hyp2" else "hyp2"], axis=1).tolist()

    print()
    print("Between the source and hallucination")
    avg = calculate_scores(sources, hallucinations)
    print(avg)
    
    print()
    print("Between the source and good paraphrases")
    avg = calculate_scores(sources, good_paraphrases)
    print(avg)

    print()

    print("Between the good paraohrases and hallucination")
    avg = calculate_scores(good_paraphrases, hallucinations)
    print(avg)