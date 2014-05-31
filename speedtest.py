#!/usr/bin/python
from timeit import Timer
from os import getcwd
from voxelspace_cython.benchmark import test as test_cython
from voxelspace.benchmark import test as test_cpython


def report(results):
	return '%fs' % min(results)

repeat = 4
number = 10

statement = 'benchmark()'
import_statement1 = 'from voxelspace.benchmark import benchmark'
import_statement2 = 'from voxelspace_cython.benchmark import benchmark'

print 'Testing Voxelspace (Cython)...'
test_cython()
print 'Timing Voxelspace (Cython)...'
t2 = Timer(statement, import_statement2)
print report(t2.repeat(repeat, number))

print 'Testing Voxelspace (CPython)...'
test_cpython()
print 'Timing Voxelspace (CPython)...'
t1 = Timer(statement, import_statement1)
print report(t1.repeat(repeat, number))
