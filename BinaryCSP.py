from collections import deque
from unittest import util
import Queue
"""
	Base class for unary constraints
	Implement isSatisfied in subclass to use
"""
class UnaryConstraint:
	def __init__(self, var):
		self.var = var

	def isSatisfied(self, value):
		util.raiseNotDefined()

	def affects(self, var):
		return var == self.var


"""	
	Implementation of UnaryConstraint
	Satisfied if value does not match passed in paramater
"""
class BadValueConstraint(UnaryConstraint):
	def __init__(self, var, badValue):
		self.var = var
		self.badValue = badValue

	def isSatisfied(self, value):
		return not value == self.badValue

	def __repr__(self):
		return 'BadValueConstraint (%s) {badValue: %s}' % (str(self.var), str(self.badValue))


"""	
	Implementation of UnaryConstraint
	Satisfied if value matches passed in paramater
"""
class GoodValueConstraint(UnaryConstraint):
	def __init__(self, var, goodValue):
		self.var = var
		self.goodValue = goodValue

	def isSatisfied(self, value):
		return value == self.goodValue

	def __repr__(self):
		return 'GoodValueConstraint (%s) {goodValue: %s}' % (str(self.var), str(self.goodValue))


"""
	Base class for binary constraints
	Implement isSatisfied in subclass to use
"""
class BinaryConstraint:
	def __init__(self, var1, var2):
		self.var1 = var1
		self.var2 = var2

	def isSatisfied(self, value1, value2):
		util.raiseNotDefined()

	def affects(self, var):
		return var == self.var1 or var == self.var2

	def otherVariable(self, var):
		if var == self.var1:
			return self.var2
		return self.var1


"""
	Implementation of BinaryConstraint
	Satisfied if both values assigned are different
"""
class NotEqualConstraint(BinaryConstraint):
	def isSatisfied(self, value1, value2):
		if value1 == value2:
			return False
		return True

	def __repr__(self):
		return 'NotEqualConstraint (%s, %s)' % (str(self.var1), str(self.var2))


class ConstraintSatisfactionProblem:
	"""
	Structure of a constraint satisfaction problem.
	Variables and domains should be lists of equal length that have the same order.
	varDomains is a dictionary mapping variables to possible domains.

	Args:
		variables (list<string>): a list of variable names
		domains (list<set<value>>): a list of sets of domains for each variable
		binaryConstraints (list<BinaryConstraint>): a list of binary constraints to satisfy
		unaryConstraints (list<BinaryConstraint>): a list of unary constraints to satisfy
	"""
	def __init__(self, variables, domains, binaryConstraints = [], unaryConstraints = []):
		self.varDomains = {}
		for i in xrange(len(variables)):
			self.varDomains[variables[i]] = domains[i]
		self.binaryConstraints = binaryConstraints
		self.unaryConstraints = unaryConstraints

	def __repr__(self):
		return '---Variable Domains\n%s---Binary Constraints\n%s---Unary Constraints\n%s' % ( \
			''.join([str(e) + ':' + str(self.varDomains[e]) + '\n' for e in self.varDomains]), \
			''.join([str(e) + '\n' for e in self.binaryConstraints]), \
			''.join([str(e) + '\n' for e in self.binaryConstraints]))


class Assignment:
	"""
	Representation of a partial assignment.
	Has the same varDomains dictionary stucture as ConstraintSatisfactionProblem.
	Keeps a second dictionary from variables to assigned values, with None being no assignment.

	Args:
		csp (ConstraintSatisfactionProblem): the problem definition for this assignment
	"""
	def __init__(self, csp):
		self.varDomains = {}
		for var in csp.varDomains:
			self.varDomains[var] = set(csp.varDomains[var])
		self.assignedValues = { var: None for var in self.varDomains }

	"""
	Determines whether this variable has been assigned.

	Args:
		var (string): the variable to be checked if assigned
	Returns:
		boolean
		True if var is assigned, False otherwise
	"""
	def isAssigned(self, var):
		return self.assignedValues[var] != None

	"""
	Determines whether this problem has all variables assigned.

	Returns:
		boolean
		True if assignment is complete, False otherwise
	"""
	def isComplete(self):
		for var in self.assignedValues:
			if not self.isAssigned(var):
				return False
		return True

	"""
	Gets the solution in the form of a dictionary.

	Returns:
		dictionary<string, value>
		A map from variables to their assigned values. None if not complete.
	"""
	def extractSolution(self):
		if not self.isComplete():
			return None
		return self.assignedValues

	def __repr__(self):
		return '---Variable Domains\n%s---Assigned Values\n%s' % ( \
			''.join([str(e) + ':' + str(self.varDomains[e]) + '\n' for e in self.varDomains]), \
			''.join([str(e) + ':' + str(self.assignedValues[e]) + '\n' for e in self.assignedValues]))



####################################################################################################


"""
	Checks if a value assigned to a variable is consistent with all binary constraints in a problem.
	Do not assign value to var. Only check if this value would be consistent or not.
	If the other variable for a constraint is not assigned, then the new value is consistent with the constraint.

	Args:
		assignment (Assignment): the partial assignment
		csp (ConstraintSatisfactionProblem): the problem definition
		var (string): the variable that would be assigned
		value (value): the value that would be assigned to the variable
	Returns:
		boolean
		True if the value would be consistent with all currently assigned values, False otherwise
"""
def consistent(assignment, csp, var, value):
	"""Question 1"""
	"""YOUR CODE HERE"""
	binConstraints = csp.binaryConstraints
	for x in binConstraints:
		if x.affects(var):
			if not x.isSatisfied(assignment.assignedValues[x.otherVariable(var)], value) and assignment.isAssigned(x.otherVariable(var)):
				return False
	return True


"""
	Recursive backtracking algorithm.
	A new assignment should not be created. The assignment passed in should have its domains updated with inferences.
	In the case that a recursive call returns failure or a variable assignment is incorrect, the inferences made along
	the way should be reversed. See maintainArcConsistency and forwardChecking for the format of inferences.

	Examples of the functions to be passed in:
	orderValuesMethod: orderValues, leastConstrainingValuesHeuristic
	selectVariableMethod: chooseFirstVariable, minimumRemainingValuesHeuristic
	Args:
		assignment (Assignment): a partial assignment to expand upon
		csp (ConstraintSatisfactionProblem): the problem definition
		orderValuesMethod (function<assignment, csp, variable> returns list<value>): a function to decide the next value to try
		selectVariableMethod (function<assignment, csp> returns variable): a function to decide which variable to assign next
	Returns:
		Assignment
		A completed and consistent assignment. None if no solution exists.
"""
def recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod):
	"""Question 1"""
	"""YOUR CODE HERE"""
	if assignment.isComplete() and consistent(assignment, csp, orderValuesMethod, selectVariableMethod):
		return assignment
	var = selectVariableMethod(assignment, csp)
	for value in orderValuesMethod(assignment, csp, var):
		if consistent(assignment, csp, var, value):
			assignment.assignedValues[var] = value
			result = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod)
			if result is not None:
				return result
			assignment.assignedValues[var] = None
	return None

"""
	Uses unary constraints to eleminate values from an assignment.

	Args:
		assignment (Assignment): a partial assignment to expand upon
		csp (ConstraintSatisfactionProblem): the problem definition
	Returns:
		Assignment
		An assignment with domains restricted by unary constraints. None if no solution exists.
"""
def eliminateUnaryConstraints(assignment, csp):
	domains = assignment.varDomains
	for var in domains:
		for constraint in (c for c in csp.unaryConstraints if c.affects(var)):
			for value in (v for v in list(domains[var]) if not constraint.isSatisfied(v)):
				domains[var].remove(value)
				if len(domains[var]) == 0:
					# Failure due to invalid assignment
					return None
	return assignment


"""
	Trivial method for choosing the next variable to assign.
	Uses no heuristics.
"""
def chooseFirstVariable(assignment, csp):
	for var in csp.varDomains:
		if not assignment.isAssigned(var):
			return var


"""
	Selects the next variable to try to give a value to in an assignment.
	Uses minimum remaining values heuristic to pick a variable. Use degree heuristic for breaking ties.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
	Returns:
		the next variable to assign
"""
def determineConstraintCount(var, csp):
	k = 0
	for x in csp.binaryConstraints:
		if x.affects(var):
			k += 1
	return k

def minimumRemainingValuesHeuristic(assignment, csp):
	nextVar = None
	domains = assignment.varDomains
	"""Question 2"""
	"""YOUR CODE HERE"""
	listy = []
	for x in domains:
		if not assignment.isAssigned(x):
			if len(listy) == 0:
				nextVar = x
				listy.append(nextVar)
			else:
				if len(domains[listy[0]]) > len(domains[x]):
					if len(listy) > 1:
						listy = []
						listy.append("Prevent KeyError")
					nextVar = x
					listy[0] = nextVar
				elif len(domains[listy[0]]) == len(domains[x]):
					listy.append(x)
	if len(listy) > 1:
		k = determineConstraintCount(listy[0], csp)
		for x in listy:
			d = determineConstraintCount(x, csp)
			if d > k:
				nextVar = x
				k = d
	return nextVar
"""
	Trivial method for ordering values to assign.
	Uses no heuristics.
"""
def orderValues(assignment, csp, var):
	return list(assignment.varDomains[var])

def getUnassignedNeighbors(assignment, csp, var):
	constraints = csp.binaryConstraints
	neighbors = []
	for x in constraints:
		if x.affects(var):
			neighbor = x.otherVariable(var)
			if not assignment.isAssigned(neighbor):
				neighbors.append(neighbor)
	return neighbors
"""
	Creates an ordered list of the remaining values left for a given variable.
	Values should be attempted in the order returned.
	The least constraining value should be at the front of the list.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
		var (string): the variable to be assigned the values
	Returns:
		list<values>
		a list of the possible values ordered by the least constraining value heuristic
"""
def leastConstrainingValuesHeuristic(assignment, csp, var):
	import operator
	values = list(assignment.varDomains[var])
	"""Hint: Creating a helper function to count the number of constrained values might be useful"""
	"""Question 3"""
	"""YOUR CODE HERE"""
	dictdog = {}
	vals = [x for x in values if consistent(assignment, csp, var, x)]
	for y in vals:
		count = 0
		assignment.assignedValues[var] = y
		neighbors = getUnassignedNeighbors(assignment, csp, var)
		if len(neighbors) == 0:
			break
		else:
			for x in neighbors:
				for k in list(assignment.varDomains[x]):
					if consistent(assignment, csp, x, k):
						count -= 1
			dictdog[y] = count
	assignment.assignedValues[var] = None
	if len(dictdog) == 0:
		return values
	sorted_dog = sorted(dictdog.items(), key=operator.itemgetter(1))
	return [val[0] for val in sorted_dog]


"""
	Trivial method for making no inferences.
"""
def noInferences(assignment, csp, var, value):
	return set([])


"""
	Implements the forward checking algorithm.
	Each inference should take the form of (variable, value) where the value is being removed from the
	domain of variable. This format is important so that the inferences can be reversed if they
	result in a conflicting partial assignment. If the algorithm reveals an inconsistency, any
	inferences made should be reversed before ending the function.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
		var (string): the variable that has just been assigned a value
		value (string): the value that has just been assigned
	Returns:
		set<tuple<variable, value>>
		the inferences made in this call or None if inconsistent assignment
"""
def forwardChecking(assignment, csp, var, value):
	inferences = set([])
	domains = assignment.varDomains
	"""Question 4"""
	"""YOUR CODE HERE"""
	if not consistent(assignment, csp, var, value):
		return None
	neighbors = getUnassignedNeighbors(assignment, csp, var)
	for x in neighbors:
		for k in list(assignment.varDomains[x]):
			if not consistent(assignment, csp, x, k):
				inferences.add((x, k))
				assignment.varDomains[x].remove(k)
				if len(assignment.varDomains[x]) == 0:
					for i in inferences:
						assignment.varDomains[i[0]].add(i[1])
					return None
	return inferences

"""
	Recursive backtracking algorithm.
	A new assignment should not be created. The assignment passed in should have its domains updated with inferences.

	In the case that a recursive call returns failure or a variable assignment is incorrect, the inferences made along
	the way should be reversed. See maintainArcConsistency and forwardChecking for the format of inferences.


	Examples of the functions to be passed in:
	orderValuesMethod: orderValues, leastConstrainingValuesHeuristic
	selectVariableMethod: chooseFirstVariable, minimumRemainingValuesHeuristic
	inferenceMethod: noInferences, maintainArcConsistency, forwardChecking


	Args:
		assignment (Assignment): a partial assignment to expand upon
		csp (ConstraintSatisfactionProblem): the problem definition
		orderValuesMethod (function<assignment, csp, variable> returns list<value>): a function to decide the next value to try
		selectVariableMethod (function<assignment, csp> returns variable): a function to decide which variable to assign next
		inferenceMethod (function<assignment, csp, variable, value> returns set<variable, value>): a function to specify what type of inferences to use
				Can be forwardChecking or maintainArcConsistency
	Returns:
		Assignment

		A completed and consistent assignment. None if no solution exists.
"""
def recursiveBacktrackingWithInferences(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod):
	"""Question 4"""
	"""YOUR CODE HERE"""
	if assignment.isComplete() and consistent(assignment, csp, orderValuesMethod, selectVariableMethod):
		return assignment
	var = selectVariableMethod(assignment, csp)
	for value in orderValuesMethod(assignment, csp, var):
		if consistent(assignment, csp, var, value):
			assignment.assignedValues[var] = value
			inference = inferenceMethod(assignment, csp, var, value)
			if inference is not None:
				for i in inference:
					assignment.varDomains[i[0]].add(i[1])
				result = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod)
				if result is not None:
					return result
			assignment.assignedValues[var] = None
	return None


"""
	Helper funciton to maintainArcConsistency and AC3.
	Remove values from var2 domain if constraint cannot be satisfied.
	Each inference should take the form of (variable, value) where the value is being removed from the
	domain of variable. This format is important so that the inferences can be reversed if they
	result in a conflicting partial assignment. If the algorithm reveals an inconsistency, any
	inferences made should be reversed before ending the fuction.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
		var1 (string): the variable with consistent values
		var2 (string): the variable that should have inconsistent values removed
		constraint (BinaryConstraint): the constraint connecting var1 and var2
	Returns:
		set<tuple<variable, value>>
		the inferences made in this call or None if inconsistent assignment
"""
def revise(assignment, csp, var1, var2, constraint):
	inferences = set([])
	"""Question 5"""
	"""YOUR CODE HERE"""
	for x in assignment.varDomains[var2]:
		works = False
		for y in assignment.varDomains[var1]:
			if constraint.isSatisfied(x, y):
				works = True
		if not works:
			inferences.add((var2, x))
	for k in inferences:
		assignment.varDomains[var2].remove(k[1])
	if len(assignment.varDomains[var2]) == 0:
		for i in inferences:
			assignment.varDomains[var2].add(i[1])
		return None
	return inferences

def getNeighborsWithConstraint(csp, var):
	constraints = csp.binaryConstraints
	neighbors = []
	for x in constraints:
		if x.affects(var):
			neighbor = x.otherVariable(var)
			neighbors.append((neighbor, x))
	return neighbors

"""
	Implements the maintaining arc consistency algorithm.
	Inferences take the form of (variable, value) where the value is being removed from the
	domain of variable. This format is important so that the inferences can be reversed if they
	result in a conflicting partial assignment. If the algorithm reveals an inconsistency, and
	inferences made should be reversed before ending the fuction.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
		var (string): the variable that has just been assigned a value
		value (string): the value that has just been assigned
	Returns:
		set<<variable, value>>
		the inferences made in this call or None if inconsistent assignment
"""
def maintainArcConsistency(assignment, csp, var, value):
	inferences = set([])
	"""Hint: implement revise first and use it as a helper function"""
	"""Question 5"""
	"""YOUR CODE HERE"""
	arcs = Queue.Queue()
	for neighbor in getNeighborsWithConstraint(csp, var):
		arcs.put((var, neighbor[0], neighbor[1]))
	while not arcs.empty():
		temp = arcs.get()
		count1 = len(assignment.varDomains[temp[1]])
		currentInference =  revise(assignment, csp, temp[0], temp[1], temp[2])
		if currentInference is None:
			for j in inferences:
				assignment.varDomains[j[0]].add(j[1])
			return None
		count2 = len(assignment.varDomains[temp[1]])
		if count1 > count2:
			if len(assignment.varDomains[temp[1]]) == 0:
				for k in inferences:
					assignment.varDomains[k[0]].add(k[1])
				for i in currentInference:
					assignment.varDomains[i[0]].add(i[1])
				return None
			for n in getNeighborsWithConstraint(csp, temp[1]):
				if n[0] != temp[0]:
					arcs.put((temp[1], n[0], n[1]))
			for i in currentInference:
				inferences.add(i)
	return inferences


"""
	AC3 algorithm for constraint propogation. Used as a preprocessing step to reduce the problem
	before running recursive backtracking.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
	Returns:
		Assignment
		the updated assignment after inferences are made or None if an inconsistent assignment
"""
def AC3(assignment, csp):
	inferences = set([])
	"""Hint: implement revise first and use it as a helper function"""
	"""Question 6"""
	"""YOUR CODE HERE"""
	arcs = Queue.Queue()
	keys = assignment.varDomains.keys()
	for key in keys:
		for constraint in csp.binaryConstraints:
			if constraint.affects(key):
				arcs.put((key, constraint.otherVariable(key), constraint))
	while not arcs.empty():
		temp = arcs.get()
		count1 = len(assignment.varDomains[temp[1]])
		currentInference =  revise(assignment, csp, temp[0], temp[1], temp[2])
		if currentInference is None:
			for j in inferences:
				assignment.varDomains[j[0]].add(j[1])
			return None
		count2 = len(assignment.varDomains[temp[1]])
		if count1 > count2:
			if len(assignment.varDomains[temp[1]]) == 0:
				for k in inferences:
					assignment.varDomains[k[0]].add(k[1])
				for i in currentInference:
					assignment.varDomains[i[0]].add(i[1])
				return None
			for n in getNeighborsWithConstraint(csp, temp[1]):
				if n[0] != temp[0]:
					arcs.put((temp[1], n[0], n[1]))
			for i in currentInference:
				inferences.add(i)
	return assignment

"""
	Solves a binary constraint satisfaction problem.
	Args:
		csp (ConstraintSatisfactionProblem): a CSP to be solved
		orderValuesMethod (function): a function to decide the next value to try
		selectVariableMethod (function): a function to decide which variable to assign next
		inferenceMethod (function): a function to specify what type of inferences to use
		useAC3 (boolean): specifies whether to use the AC3 preprocessing step or not
	Returns:
		dictionary<string, value>
		A map from variables to their assigned values. None if no solution exists.
"""
def solve(csp, orderValuesMethod=leastConstrainingValuesHeuristic, selectVariableMethod=minimumRemainingValuesHeuristic, inferenceMethod=None, useAC3=True):
	assignment = Assignment(csp)

	assignment = eliminateUnaryConstraints(assignment, csp)
	if assignment == None:
		return assignment

	if useAC3:
		assignment = AC3(assignment, csp)
		if assignment == None:
			return assignment
	if inferenceMethod is None or inferenceMethod==noInferences:
		assignment = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod)
	else:
		assignment = recursiveBacktrackingWithInferences(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod)
	if assignment == None:
		return assignment

	return assignment.extractSolution()
