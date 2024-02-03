for f in *.png
do 
    convert -crop 3730x2200+0+0 ${f} ../resized/${f}
done
# convert -crop 3730x2800+0+0 003_002full.png ../resized/003_002full.png
# convert -crop 3730x2800+0+0 008_004full.png ../resized/008_004full.png
# convert -crop 3730x2800+0+0 003_002omitted.png ../resized/003_002omitted.png
