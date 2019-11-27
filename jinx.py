import os
import gdb


# Engines
#
class Engine:

  def __init__(self):
    self.data = ''
    self.func_name = ''

  def init(self, func_name):
    self.func_name = func_name

  def validate(self, data):
    return False

  def dump_data(self):
    return self.data


class MipsTail(Engine):

  def validate(self, data):

    r_move = []
    r_lw = []
    r_j = ''

    for item in data:

      if len(item) >= 4:

        if len(item) < 4 or item[2] == 'b':
          r_move = []
          r_lw = []
          r_j = ''

        opcode = ' '.join(item[2:])

        if item[2] == 'move' and item[3][:3] == 't9,':
          r_move.append(opcode)

        if item[2] == 'lw' and item[3][:2] == 'ra':
          r_lw.append(opcode)

        if item[2][:1] == 'j' and len(r_move) > 0 and len(r_lw) > 0:

          if item[3] == 't9' or item[3][:1] == 's':
            r_j = opcode

    if len(r_move) > 0 and len(r_lw) > 0 and r_j != '':

      print("+" + self.func_name + " found !!!!11111..")
      print(r_move)
      print(r_lw)
      print(r_j)
      self.data = self.func_name

      return True

    return False


# Routing
#
class Route:

  engines = {
    'mips-tail': MipsTail
  }

### End Routes


# Let's paint Your console!!
#
class Painter:

  RED = '\033[91m'
  BLUE = '\033[94m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  CYAN = '\x1b[0;36;40m'
  SILVER = '\x1b[0;37;40m'
  LIGHT_PURPLE = '\033[94m'
  PURPLE = '\033[95m'
  END = '\033[0m'

  @classmethod
  def cyan(cls, message):
    print(cls.CYAN + message + cls.END)

  @classmethod
  def silver(cls, message):
    print(cls.SILVER + message + cls.END)


class Jinx(gdb.Command):

  def __init__(self):
    super(Jinx, self).__init__(
      "jx",
      gdb.COMMAND_SUPPORT,
      gdb.COMPLETE_NONE,
      True
    )

    self.engine = False
    self.log_file = "jinx_log.txt"


  def invoke(self, args, from_tty):

    args = args.split()

    if [] == args or args[0] not in Route.engines:

      self.show_help()

    else:

      self.engine = Route.engines[args[0]]()
      self.run_search()


  def run_search(self):

    functions = gdb.execute('info functions', to_string=True).splitlines()

    for func in functions:

      func = func.split()

      # validate function name
      #
      if len(func) == 2 and func[0][:2] == '0x':

        # temp array for function data
        #
        t_data = []

        # init search engine
        self.engine.init(func[1])

        lines = gdb.execute('disas ' + func[1], to_string=True).splitlines()

        for line in lines:

          # valiate opcodes
          #
          line = line.split()

          if '0x' == line[0][:2]:
            t_data.append(line)


        # if function contains specific data - make a log
        #
        if self.engine.validate(t_data):
          self.to_log( self.engine.dump_data() )


  def to_log(self, data):
    if os.path.isfile(self.log_file):
      os.remove(self.log_file)

    if data != '':
      log = open(self.log_file, 'a')
      log.write(data)
      log.close()


  def show_help(self):
    Painter.cyan("____________ Jinx ____________\r\n")
    Painter.silver("usage: jx <option> ..\r\n")

Jinx()
