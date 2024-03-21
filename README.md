# Are Large Language Models Good at Lexical Semantics? A Case of Taxonomy Learning

This repo contains code for paper [Are Large Language Models Good at Lexical Semantics? A Case of Taxonomy Learning](google.com) published at LREC/COLING 2024.

# Data

The dataset we used could be accessed via this [link](google.com)

In the provided folder exists dataset for LLM fine-tuning on WordNet and data from Semeval-16, that we used for taxonomy construction task.

All of our data follows the same format, we have modified each test and train set to follow this format, as it is handy to use.

Each train or test set presented with ```.pickle``` format, for the ease of python usage. It is a list of python dictionaries, each dictionary represents a single object. Each object has keys and corresponding values
- case: a precise case of current object that corresponds to the the paper. More details are availible with python script ```leafer.py```. The correspodning is the following:
  - only_child_leaf: Sinle Leaves
  - only_leafs_all: Only Leaves
  - only_leafs_divided: Leaves Divided
  - leafs_and_no_leafs: Internal Nodes
  - simple_triplet_grandparent: Insertion
  - simple_triplet_2parent: Synset Mixing
  - predict_hypernym: Hypernym Prediction 
- parents: string representing hypernym
- children: string or list of string representing hyponym
- grandparents: string or list of string representing hyperhypernym
  
  One of the following could be missing in some cases where they are not applicable
- child_def: string representing definition for the hyponym
- parent_def: string representing definition for the hypernym
- grandparent_def: string representing definition for the hyperhypernym

# Pre-training with WordNet

For pre-training with instructive WordNet dataset one should simply sample data in our format or take our published set. The process of sampling and recreation of data is possible in ```DataConsructor/sample_data.ipynb``` notebook. As well we also publish created datasets and can be downloaded from Drive named ```wnet_data.tar.gz```.

### Training, Inference, Fine-tuning

To use private models, user is required to save the HF auth token in environment variable ```export HF_TOKEN=<your token>```. As well, you need to specify the home directory for caching HF, saving all outputs, trained models, etc. as ```export SAVING_DIR='/your/directory'```

To train the model in our setting one needs to simply run the ```train.py``` script with the configs, specified in ```configs/train.yml```. Every parameter is described there. It reports final metrics to WandB and prints to terminal.

To inference the pre-trained model later one can use the ```inference.py``` script with the configs in ```configs/inference.yml```. The final metrics are printed and predictions are saved in file.

To get the detailed metric report with examples one needs to run ```metrics.py``` script with the configs in ```configs/metrics.yml```. 

To fine tune the model for your dataset, you can simply treat pre-trained model as intiial checkpoint and run the ```train.py``` script with checkpoint, specified in configs.

### Taxonomy Construction

To estimate perplexity firstly the model should be saved with hugging face format and either uploaded to hugging face or stored locally. Those actions needed to properly upload model. 
Then one should run ```TExEval-2_testdata_1.2/est_ppl.py``` script with the configs ```TExEval-2_testdata_1.2/configs/ppl_est.yml```. It will save resulting perplexities in format of python dict where key is tuple (hyponym, hypernym) and value is perplexity. 

The data for perplexity estimation of TExEval in desired format is availible by the link in ```taxonomy_construction_data.tar.gz```. Raw data from TExEval are located in ```gs_taxo``` and ```gs_terms```. Data in our desired format could be accessed in directory sci or env (corresponding to dataset), in the directory named raw.

Once the perplexities are calculated, one could build the taxonomy by running ```TExEval-2_testdata_1.2/build_taxo.py``` with configs in ```TExEval-2_testdata_1.2/configs/build_taxo.yml```. The final metric will be outputed.
