import os
import csv
from rdkit import Chem
from rdkit import RDLogger
from multiprocessing import Pool

RDLogger.DisableLog('rdApp.*')

# -------------------- beta-lactam motif --------------------
#BETA_LACTAM_SMARTS = '[#6;r4]1[#6;r4][#6;r4](=O)[#7;r4]1'
#more restrictive SMARTS motif (restrict alpha carbon to C, N, O or S)
BETA_LACTAM_SMARTS = "[#6;r4]1[#6;r4]([#6,#7,#8,#16])[#6;r4](=O)[#7;r4]1"
BETA_LACTAM_QUERY = Chem.MolFromSmarts(BETA_LACTAM_SMARTS)

def is_beta_lactam(smiles: str) -> bool:
    smiles = smiles.strip()
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return False
    return mol.HasSubstructMatch(BETA_LACTAM_QUERY)

# -------------------- PubChem --------------------
def process_pubchem_line(line):
    tokens = line.strip().split(maxsplit=1)
    if len(tokens) < 2:
        return None
    cid, smiles = tokens
    if is_beta_lactam(smiles):
        return [cid, smiles]
    return None

def process_pubchem_file(file_path, output_file, n_cpus=1, print_every=1_000_000):
    hits = 0
    total = 0
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(file_path, 'r') as f_in:
        lines = f_in.readlines()

    if n_cpus > 1:
        with Pool(n_cpus) as pool:
            results = pool.map(process_pubchem_line, lines)
    else:
        results = [process_pubchem_line(l) for l in lines]

    with open(output_file, 'w', newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(['CID', 'SMILES'])
        for r in results:
            total += 1
            if r:
                hits += 1
                writer.writerow(r)
            if total % print_every == 0:
                print(f"Processed {total:,} lines, beta-lactams found: {hits}")

    print(f"PubChem finished: {hits}/{total} beta-lactams")

# -------------------- ZINC15 --------------------
def process_zinc_file(file_path, output_file):
    if not os.path.isfile(file_path):
        print(f"WARNING: File not found: {file_path}")
        return

    hits = 0
    total = 0
    with open(file_path) as f_in, open(output_file, 'a', newline='') as f_out:
        writer = csv.writer(f_out)
        for line in f_in:
            total += 1
            smiles = line.strip()
            if is_beta_lactam(smiles):
                hits += 1
                writer.writerow([smiles])
    print(f"{file_path}: {hits}/{total} beta-lactams found")

def process_zinc_group(file_list, output_file, n_cpus=1, base_dir=None):
    """
    file_list: list of filenames (can be relative)
    base_dir: optional path to prepend to relative files
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # make absolute paths
    if base_dir:
        file_list = [os.path.join(base_dir, f) if not os.path.isabs(f) else f for f in file_list]

    if n_cpus > 1:
        with Pool(n_cpus) as pool:
            pool.starmap(process_zinc_file, [(f, output_file) for f in file_list])
    else:
        for f in file_list:
            process_zinc_file(f, output_file)

# -------------------- main --------------------
def main(args):
    # --- PubChem ---
    if args.pubchem_input:
        process_pubchem_file(args.pubchem_input, args.pubchem_output, n_cpus=args.n_cpus)

    # --- ZINC15 ---
    if args.zinc_file_list:
        with open(args.zinc_file_list, 'r') as f:
            file_list = [line.strip() for line in f]

        process_zinc_group(
            file_list,
            args.zinc_output,
            n_cpus=args.n_cpus,
            base_dir=args.zinc_base_dir
        )

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--pubchem_input', default=None)
    parser.add_argument('--pubchem_output', default='./beta_lactams_pubchem.csv')
    parser.add_argument('--zinc_file_list', default=None)
    parser.add_argument('--zinc_output', default='./beta_lactams_zinc.csv')
    parser.add_argument('--zinc_base_dir', default=None, help="Optional base dir to prepend to ZINC files")
    parser.add_argument('--n_cpus', type=int, default=1)
    args = parser.parse_args()
    main(args)