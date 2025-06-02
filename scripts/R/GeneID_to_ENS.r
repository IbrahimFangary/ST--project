# Install the EnsDb.Hsapiens.v79 package (only run this once if not installed)
# BiocManager::install("EnsDb.Hsapiens.v79")

# Load the Ensembl database package for Homo sapiens
library(EnsDb.Hsapiens.v79)

# Check the class of the geneSymbols object (for debugging or validation)
class(geneSymbols)

# List files inside the compressed features.tsv.gz directory
list.files('/kaggle/input/honda/single_cell/features.tsv.gz')

# Read the gene feature file (tab-separated, no header)
feature = read.csv('/kaggle/input/honda/single_cell/features.tsv.gz', sep= '\t', header=FALSE)

# Convert the first column (gene IDs) into a character vector
geneSymbols <- as.character(feature$V1)

# Print the data frame for inspection
feature

# Show how many gene symbols were read
length(geneSymbols)

# -- Optionally convert Ensembl gene IDs to gene symbols --
# ensembl.genes <- c("ENSG00000150676", "ENSG00000099308", ... )
# geneIDs1 <- ensembldb::select(EnsDb.Hsapiens.v79, keys= ensembl.genes, keytype = "GENEID", columns = c("SYMBOL","GENEID"))

# -- Convert gene symbols to Ensembl gene IDs --
# Define a list of gene symbols (optional example)
# geneSymbols <-  c('DDX26B','CCDC83', 'MAST3', 'RPL11', 'ZDHHC20', 'LUC7L3', 'SNORD49A', 'CTSH', 'ACOT8')

# Query the database to convert gene symbols to Ensembl gene IDs
geneIDs2 <- ensembldb::select(EnsDb.Hsapiens.v79, keys= geneSymbols, keytype = "SYMBOL", columns = c("SYMBOL","GENEID"))

# Add a column named "Gene Expression" with a constant value for all rows
geneIDs2$'Gene Expression' = 'Gene Expression'

# Reorder columns to match desired format: GENEID, SYMBOL, Gene Expression
geneIDs2 <- geneIDs2[, c('GENEID','SYMBOL','Gene Expression')]

# Display the first few rows of the new table
head(geneIDs2) 

# Save the table as a gzipped TSV file with no row or column names and no quotes
write.table(geneIDs2, file = "feature.tsv.gz", sep = "\t", row.names = FALSE, col.names = FALSE, quote = FALSE)

     
