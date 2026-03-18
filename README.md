# β-Lactam Substructure Screening
Identifies β-lactam compounds in large molecular datasets (ZINC15, PubChem) 
using RDKit substructure matching with multiprocessing support.

## Context
This script was developed to assess whether the MolFormer pretraining datasets 
(ZINC15, PubChem) contain β-lactam compounds, as part of evaluating the ability 
of S3-GFN to rediscover β-lactam chemistry [[1]](https://arxiv.org/abs/2602.04119).


## β-Lactam SMARTS definition
We use the following β-Lactam SMARTS pattern, which enforces a substituent 
(C, N, O or S) at the α-carbon — consistent with clinically relevant β-lactams:
```
[#6;r4]1[#6;r4]([#6,#7,#8,#16])[#6;r4](=O)[#7;r4]1
```

## Results
| Dataset | Total molecules | β-Lactam hits | Unique hits |
|---------|----------------|---------------|-------------|
| ZINC15  | ~1.1 billion   | 300,847       | 300,845     |
| PubChem | ~110 million   | 300,173       | 204,403     |

## Usage - Quick test
Small fake datasets are provided to test the script without downloading 
the full PubChem or ZINC15 datasets:
```bash
# test on fake PubChem
python beta_lactams_screening.py \
    --pubchem_input data/pubchem/fake_pubchem.smi \
    --pubchem_output data/pubchem/test_output.csv

# test on fake ZINC15
python beta_lactams_screening.py \
    --zinc_file_list data/ZINC/fake_zinc_files_names.txt \
    --zinc_base_dir data/ZINC \
    --zinc_output data/ZINC/test_output.csv
```

## Requirements
- Python 3.10+
- RDKit

## Installation
```bash
conda create -n beta_lactam python=3.10
conda activate beta_lactam
conda install -c conda-forge rdkit
```

## License
MIT

**References**  
[1] [S3-GFN preprint](https://arxiv.org/abs/2602.04119)
