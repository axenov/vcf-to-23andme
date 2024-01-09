def split_genotypes(input_file, output_file1, output_file2):
    with open(input_file, 'r') as infile, open(output_file1, 'w') as outfile1, open(output_file2, 'w') as outfile2:
        # Read and write comments
        comments = []
        line = infile.readline()
        while line.startswith('#'):
            comments.append(line)
            line = infile.readline()

        lines = [line]

        # Write comments to output files
        outfile1.writelines(comments)
        outfile2.writelines(comments)

        for line in infile:
            lines.append(line)
            
        for line in lines:
            parts = line.strip().split('\t')

            rsid = parts[0]
            chromosome = parts[1]
            position = parts[2]
            genotype = parts[3]

            if chromosome not in ["X", "Y", "MT"]:
                # Create separate lines for each allele
                allele1_line = '\t'.join([rsid, chromosome, position, genotype[0]]) + '\n'
                allele2_line = '\t'.join([rsid, chromosome, position, genotype[1]]) + '\n'

                # Write lines to the respective output files
                outfile1.write(allele1_line)
                outfile2.write(allele2_line)

# Example usage
input_file = 'imputed_23andme_full_short.txt'
output_file1 = 'parent_1_imputed_23andme_full_short.txt'
output_file2 = 'parent_2_imputed_23andme_full_short.txt'

split_genotypes(input_file, output_file1, output_file2)
