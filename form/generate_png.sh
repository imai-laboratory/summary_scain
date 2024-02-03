for i in `seq 9 `
do
    for j in `seq 0 7`
    do
	tex2img --top-margin 100 --left-margin 100 --right-margin 100 --bottom-margin 100 --no-transparent ./00${i}_00${j}full.tex ./png/00${i}_00${j}full.png
    done
done
