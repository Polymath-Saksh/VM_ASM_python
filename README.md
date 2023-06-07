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
## Limitations

Currently, this translator supports the following commands:
- Push and Pop commands
- Arithmetic commands: `add`, `sub`, `neg`, `eq`, `gt`, `lt`, `and`, `or`, `not`
- Branching commands: `label`, `goto`, `if-goto`

Functionality for Function commands (`function`, `call`) will be added in future commits.

The translated ASM code will be saved in a file with the name '`output.asm`' in the root directory of this translator.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Written by Saksham Kumar (polymath_saksh)

© 2023 Saksham Kumar
