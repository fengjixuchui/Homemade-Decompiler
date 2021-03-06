import pwn


class BaseAsmFile(object):
	"""
	Abstract class to describe an ASM file.
	The inheriting subclasses should receive only a binary file name and disassemble it in order to implement this
	class' functions.
	"""

	def __init__(self, bin_filename):
		"""
		:param bin_filename: The binary filename.
		:type bin_filename: C{str}
		"""
		self._filename = bin_filename

	def get_func_address_size_and_content(self, func_name):
		"""
		Get the address, size and content of the function.

		:param func_name: The function name
		:type func_name: str
		:return: The address of the function, its size (in bytes) and its content
		:rtype: tuple(int, int, str)
		"""
		pass
	
	def get_func_name_by_address(self, address):
		raise NotImplementedException()
	
	def get_plt_name(self, address):
		raise NotImplementedException()

class AsmElfFile(BaseAsmFile):
	def __init__(self, elf_filename):
		"""
		:param elf_filename: The ELF filename
		:type elf_filename: str
		"""
		super(AsmElfFile, self).__init__(elf_filename)
		self._file = pwn.ELF(elf_filename)

	def get_func_address_size_and_content(self, func_name):
		"""
		Get the function's address, size and instructions.
		:param func_name: The function name.
		:type func_name: str
		:return: The function's address, size and instructions
		:rtype: tuple(int, int, str)
		"""
		func = self._file.functions[func_name]
		return func.address, func.size, self._file.disasm(func.address, func.size)
	
	def get_func_name_by_address(self, address):
		for func_name, func in self._file.functions.items():
			if func.address == address:
				return func_name

		return None	
	
	def get_plt_name(self, address):
		for plt_name, plt_address in self._file.plt.items():
			if plt_address == address:
				return plt_name

		return None




