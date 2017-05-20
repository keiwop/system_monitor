import config



class Formatting:
	multiples = ["", "K", "M", "G", "T", "P"]
	
	units_sizes = {	"B": "iec", 
					"Bps": "iec",
					"B/s": "iec",
					"bps": "metric",
					"b/s": "metric"}
	
	units_prefixes = {	"iec": (1024, "i", ""),
						"metric": (1000, "", "")}
	
	def __init__(self):
		pass

	def formatter(self, value, unit="B", prefix=None, precision=.1, show_unit=True):
		multiplier = 1000
		f_prefix = ""
		base_prefix = ""
		
		if unit in self.units_sizes:
			if prefix is None:
				prefix = self.units_sizes[unit]
			if prefix in self.units_prefixes:
				multiplier, f_prefix, base_prefix = self.units_prefixes[prefix]
		
		formatted_size = f"0{self.multiples[0]}"
		if config.show_unit_for_zero:
			formatted_size += f" {unit}"
		
		for i, multiple in enumerate(reversed(self.multiples)):
			index = len(self.multiples) - 1 - i
			tmp_size = value / (multiplier ** index)
			value = value % int(multiplier ** index)
			
			if int(tmp_size) > 0:
				if index == 0:
					f_prefix = base_prefix
				formatted_size = f"{tmp_size:{precision}f}"
				if show_unit:
					formatted_size += f" {multiple}{f_prefix}{unit}"
				break
		
		return formatted_size
	
	def size(self, value, unit="B", prefix=None, precision=.2, show_unit=True):
		return self.formatter(value, unit, prefix, precision, show_unit)
			
	def speed(self, value, unit="B/s", prefix=None, precision=.2, show_unit=True):
		return self.formatter(value, unit, prefix, precision, show_unit)

	def perc(self, value, precision=.1):
		return f"{value:{precision}f}%"
