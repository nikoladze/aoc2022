animation.gif: frames/done
	ffmpeg -i "frames/%03d.png" animation.gif

frames/done: trace.pkl animate.py
	mkdir -p frames
	./animate.py
	touch frames/done

trace.pkl: trace.py solver.py
	./trace.py
