# VCF-to-23andMe
These scripts convert a Sanger Imputation Service output into the 23andMe V3 raw data format.

data_to_db.py is used to convert the VCF file and any additional 23andMe raw data file (adds 23andMe indentifiers) into an indexed SQLite3 database for quick searching. db_to_23.py then inserts genotypes into the blank file retrieved from the database by chromosome, position and identifier.

The data_to_db.py script accepts both compressed and uncompressed data files.

## Requirements
* [Sanger Imputation Service](https://www.sanger.ac.uk/tool/sanger-imputation-service/)
* Python3
* [bcftools](https://www.htslib.org/download/)
* [plink2](https://www.cog-genomics.org/plink2/)

## Usage

```bash
cd /path/to/imputed.vcfs
# Merge chromosomes
bcftools concat -Oz 1.vcf.gz 2.vcf.gz 3.vcf.gz 4.vcf.gz 5.vcf.gz 6.vcf.gz 7.vcf.gz 8.vcf.gz 9.vcf.gz 10.vcf.gz 11.vcf.gz 12.vcf.gz 13.vcf.gz 14.vcf.gz 15.vcf.gz 16.vcf.gz 17.vcf.gz 18.vcf.gz 19.vcf.gz 20.vcf.gz 21.vcf.gz 22.vcf.gz X.vcf.gz > wgs.vcf.gz
# Select identified SNPs
bcftools view -Oz -e 'ID=="."' -o filtered_wgs.vcf.gz wgs.vcf.gz
# Select good SNPs (optional)
# bcftools view -Oz -i 'INFO>0.95' -o filtered_second_wgs.vcf.gz filtered_wgs.vcf.gz
# Select good and rare SNPs (optional)
# bcftools view -Oz -i 'INFO>0.95' -q 0.05:minor -o filtered_second_wgs.vcf.gz filtered_wgs.vcf.gz

# Transofrm the whole genome into the 23andMe format (optional)
cd /path/to/plink
./plink --vcf /path/to/imputed.vcfs/filtered_wgs.vcf.gz  --snps-only --recode 23 --out imputed_23andme_full

cd /path/to/vcf-to-23andme
# Construct a short file in 23andMe format
python data_to_db.py /path/to/original/23andme_v5_original.txt 23andme genome.db # (optional)
python data_to_db.py /path/to/imputed.vcfs/filtered_wgs.vcf.gz vcf genome.db
# Use all_templates_merged_blank.tsv to consider all SNPs from 23andMe v3,v4 and v5, AncestryDNA v1 and v2,
# FTDNA v1 and v2, Tellmegen v1 and v2, LivingDNA, SelfDecode v1 and MyHerritage v2.
# Alternatively use 23andme_v3_blank.tsv, 23andme_v5_blank.txt or 23andme_merged_v3v4v5_blank.tsv
python db_to_23.py genome.db all_templates_merged_blank.tsv imputed_23andme_full_short.txt

# If phasing was performed before imputation you can run split_parents.py to split
# imputed_23andme_full_short.txt into parent 1 and parent 2 files. 
# These files can be later used in the DNAGenics's Admixture Studio and G25 Studio
python split_parents.py 
```

