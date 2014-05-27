find ./ -not -path "./.git/*" -not -name "*.pyc" -and -type f >> files
for file in `cat files` ; do cat $file; done | wc -l
rm files