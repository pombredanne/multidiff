#!/usr/bin/python3
import argparse
from multidiff import MultidiffModel, StreamView, SocketController, FileController, StdinController

parser = argparse.ArgumentParser(
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description="""
  \x1b[1mN E O N S E N S E\x1b[0m
  augmentations inc
  ┌───────────────┐
  │ \x1b[1mM  U  L  T  I\x1b[0m │
  │ \x1b[1mD   I   F   F\x1b[0m │
  │ sensor module │
  └───────────────┘
""")

parser.add_argument('file',
	type=str,
	nargs='*',
	help='file or directory to include in multidiff')

parser.add_argument('-m', '--mode',
	dest='mode',
	default='sequence',
	help='mode of operation, either "baseline" or "sequence"')

parser.add_argument('-o','--outformat',
	dest='outformat',
	default='hexdump',
	type=str,
	help='output data format: utf8, hex, or hexdump (default)')

parser.add_argument('-i','--informat',
	dest='informat',
	type=str,
	help='input data format: utf8 (stdin default), raw (file default), hex, or json (server default)')

parser.add_argument('-s','--stdin',
	dest='stdin',
	action='store_true',
	help='read data from stdin')

parser.add_argument('-p','--port',
	dest='port',
	default=0,
	type=int,
	help='start a local socket server on a given port')

if __name__ == '__main__':
	args = parser.parse_args()
	m = MultidiffModel()
	v = StreamView(m, encoding=args.outformat)
	
	if len(args.file) > 0:
		if not args.informat:
			f = FileController(m, 'raw')
		else:
			f = FileController(m, args.informat)
		f.add_paths(args.file)
	if args.stdin:
		if not args.informat:
			stdin = StdinController(m, 'utf8')
		else:
			stdin = StdinController(m, args.informat)
		stdin.read_lines()
	if args.port != 0:
		if not args.informat:
			server = SocketController(('127.0.0.1', args.port), m, 'json')
		else:
			server = SocketController(('127.0.0.1', args.port), m, args.informat)
		server.serve_forever()
