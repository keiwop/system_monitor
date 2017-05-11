

class Formatting:
	
	units_size_iec = ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]
	units_size_metric = ["B", "KB", "MB", "GB", "TB", "PB"]
	
	def __init__(self):
		pass
	
	def size(self, in_size, unit="iec"):
		if unit == "iec":
			multiplier = 1024
			units_list = self.units_size_iec
		elif unit == "metric":
			multiplier = 1000
			units_list = self.units_size_metric
		
		formatted_size = f"0{units_list[0]}"
		
		for i, unit in enumerate(reversed(units_list)):
			index = len(units_list) - 1 - i
			tmp_size = in_size / (multiplier ** index)
			in_size = in_size % int(multiplier ** index)
			
			if int(tmp_size) > 0:
				formatted_size = f"{tmp_size:.1f} {unit}"
				break
		return formatted_size
			
			
