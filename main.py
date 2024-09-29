import argparse
from src.eval_metric import score_all_free
import pandas as pd
from statistics import mean
from random import shuffle
import json

parser = argparse.ArgumentParser()
parser.add_argument(
    "--model_type_parascore",
    type=str,
    default="bert-base-uncased",
    required=False,
    help="pretrained model type or path to pretrained model",
)
parser.add_argument(
    "--model_type_selfibleu",
    type=str,
    default="bert-base-uncased",
    required=False,
    help="pretrained model type or path to pretrained model",
)
parser.add_argument(
    "--model_type_bert",
    type=str,
    default="bert-base-uncased",
    required=False,
    help="pretrained model type or path to pretrained model",
)

parser.add_argument(
    "--model_type_nli",
    type=str,
    default="MoritzLaurer/DeBERTa-v3-base-mnli-fever-docnli-ling-2c",
    required=False,
    help="pretrained model type or path to pretrained model",
)
parser.add_argument(
    "--model_type_emb",
    type=str,
    default="sentence-transformers/all-mpnet-base-v2",
    required=False,
    help="pretrained model type or path to pretrained model",
)


parser.add_argument("--batch_size", type=int, default=16,  required=False)
parser.add_argument("--datafile", type=str, required=True, help="data file (csv, comma separated)")
parser.add_argument("--outputfile", type=str, required=True, help="output filename for results")
parser.add_argument("--alpha", type=float, required=False, default="0.2", help="alpha in ibleu")
parser.add_argument("--beta", type=float, required=False, default="3", help="beta in selfibleu")
parser.add_argument(
    "--weight", type=float, required=False, default=0.0, help="weight in free parascore"
)

args = parser.parse_args()


def calculate_scores(query: list, hyp: list) -> dict:
    results = {}
    for i in available_metrics:
        try:
            args.metric = i
            out = score_all_free(args, query, hyp)
            results[i] = out
        except BaseException as err:
            print("could not calculate", i)
            print("Error:", err)

    average = {}
    for k, v in results.items():
        average[k] = mean(v)
    return average


if __name__ == "__main__":
    available_metrics = [
        "bleu",
        "meteor",
        "rougeL",
        "rouge1",
        "rouge2",
        "selfibleu",
        "parascore",
        # "bartscore", # no path to pretrained model
        "emb-manhattan",
        "emb-cosine",
        "emb-dot",
        "emb-euclidean",
        "nli",
    ]

    data = pd.read_csv(args.datafile, sep=",")
    sources = data["source"].tolist()
    hallucinations = data.apply(lambda row: row[row["label"]], axis=1).tolist()
    good_paraphrases = data.apply(
        lambda row: row["hyp1" if row["label"] == "hyp2" else "hyp2"], axis=1
    ).tolist()

    output = {}
    print("Examples:", len(sources))
    print("Calculating similarities between the sources and hallucination....")
    avg = calculate_scores(sources, hallucinations)
    output["sources-hallucinations"] = avg
    print("Calculating similarities vetween the sources and good paraphrases")
    avg = calculate_scores(sources, good_paraphrases)
    output["sources-paraphrases"] = avg
    print("Calculating similarities between the good paraphrases and hallucination")
    avg = calculate_scores(good_paraphrases, hallucinations)
    output["paraphrases-hallucinations"] = avg
    print("Control: Calculating similarities between the sources and hallucination shuffled")
    shuffle(hallucinations)
    avg = calculate_scores(sources, hallucinations)
    output["sources-hallucinations_shuffled"] = avg

    for k, v in output.items():
        print(k)
        for metric, score in v.items():
            print(metric, score)
        print()

    with open(args.outputfile, "w+") as f:
        f.write(json.dumps(output, indent=3))
