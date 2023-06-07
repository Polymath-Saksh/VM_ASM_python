# VM_ASM_python

A Virtual Machine to ASM translator in Python Language.

## Usage

To translate a VM file to ASM, run the following command:

```
python translator.py <filename or filelocation>
```

Example usage:

```
python translator.py test.vm
python translator.py /path/test.vm
python translator.py "A:/User/...../test.vm"
```

The translated ASM code will be saved in a file with the same name as the input file, but with a `.asm` extension.

## Limitations

Currently, this translator supports the following commands:
- Push and Pop commands
- Arithmetic commands: `add`, `sub`, `neg`, `eq`, `gt`, `lt`, `and`, `or`, `not`
- Branching commands: `label`, `goto`, `if-goto`

Functionality for Function commands (`function`, `call`) will be added in future commits.

Please note that the translator may have other limitations or constraints not mentioned here.
