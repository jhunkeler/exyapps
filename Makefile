exyapps/grammar.py: yapps_grammar.g
	exyapps yapps_grammar.g exyapps/grammar.py

clean:
	rm -rf dist build
	rm -f MANIFEST
	rm -f examples/calc.py  examples/expr.py  examples/lisp.py  examples/xml.py

