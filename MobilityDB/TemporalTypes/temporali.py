from MobilityDB.TemporalTypes.temporalinst import TEMPORALINST
from MobilityDB.TemporalTypes.temporalinstants import TEMPORALINSTANTS
from MobilityDB.TimeTypes.period import PERIOD
from MobilityDB.TimeTypes.periodset import PERIODSET


class TEMPORALI(TEMPORALINSTANTS):

	def __init__(self, *argv):
		# Constructor with a single argument of type string
		self._instantList = []
		if len(argv) == 1 and isinstance(argv[0], str):
			ts = argv[0].strip()
			if ts[0] == '{' and ts[-1] == '}':
				ts = ts[1:-1]
				instants = ts.split(",")
				for inst in instants:
					self._instantList.append(TEMPORALI.ComponentValueClass(inst.strip()))
			else:
				raise Exception("ERROR: Could not parse temporal instant set value")
		# Constructor with a single argument of type list
		elif len(argv) == 1 and isinstance(argv[0], list):
			# List of strings representing instant values
			if all(isinstance(arg, str) for arg in argv[0]):
				for arg in argv[0]:
					self._instantList.append(TEMPORALI.ComponentValueClass(arg))
			# List of insant values
			elif all(isinstance(arg, TEMPORALI.ComponentValueClass) for arg in argv[0]):
				for arg in argv[0]:
					self._instantList.append(arg)
			else:
				raise Exception("ERROR: Could not parse temporal instant set value")
		# Constructor with multiple arguments
		else:
			# Arguments are of type string
			if all(isinstance(arg, str) for arg in argv):
				for arg in argv:
					self._instantList.append(TEMPORALI.ComponentValueClass(arg))
			# Arguments are of type datetime
			elif all(isinstance(arg, TEMPORALI.ComponentValueClass) for arg in argv):
				for arg in argv:
					self._instantList.append(arg)
			else:
				raise Exception("ERROR: Could not parse temporal instant set value")
		# Verify validity of the resulting instance
		if not self._valid():
			raise Exception("ERROR: The timestamps of the temporal instants must be increasing")

	def _valid(self):
		return all(x._time < y._time for x, y in zip(self._instantList, self._instantList[1:]))

	@classmethod
	def duration(cls):
		return "InstantSet"

	def getTime(self):
		"""
		Timestamp
		"""
		return PERIODSET([PERIOD(inst._time, inst._time, True, True) for inst in self._instantList])

	def period(self):
		"""
		Period on which the temporal value is defined
		"""
		return PERIOD(self.startTimestamp(), self.endTimestamp(), True, True)

	def intersectsTimestamp(self, datetime):
		"""
		Intersects timestamp
		"""
		return any(inst._time == datetime for inst in self._instantList)

	def intersectsPeriod(self, period):
		"""
		Intersects period
		"""
		return any(period.contains(inst._time) for inst in self._instantList)

	def __str__(self):
		return '{' + TEMPORALINSTANTS.__str__(self) + '}'
