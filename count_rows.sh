find ./ -not -path "./.git/*" -not -path "./.idea/*" -not -path "./docs_build/*" -not -name "*.pyc" -and -type f >> files
for file in `cat files` ; do cat $file; done | wc -l
rm files
