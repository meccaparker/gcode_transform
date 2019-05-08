import sys

# read file at path
def read_f(path):
  with open(path, "rt") as f:
    return f.read();

# write file to path
def write_f(path, contents):
  with open(path, "wt") as f:
    f.write(contents);

# write transformed gcoce to path
def write_transform(path, gcode):
  p = path.split('/') # split path up by "/"
  f_name = p[-1].split(".")[0] # get file name from text before "."
  new_path = f_name + "_3_WHEEL.gcode" # new file name
  write_f(new_path, gcode) # write file
  print("Gcode in file %s.gcode was successfully written to %s.\n" % (f_name, new_path))

# arithmetic operations for transforming x, y, z values
def transform_xyz(xyz):
  new_xyz = [0, 0, 0] # store new xyz vals in array
  x, y, z = float(xyz[0]), float(xyz[1]), float(xyz[2]); # convert to floats
  # arithmetic operations to transform from 4-wheel to 3-wheel
  new_xyz[0] = float(x);
  new_xyz[1] = round((-0.866 * x) + (0.5 * y), 4); 
  new_xyz[2] = round((0.866 * x) - (0.5 * y), 4);
  return new_xyz;

# parse an individual line of gcode
def parse_line(line):
  line = line.split(" "); # split line up by " "
  new_line = [""] * len(line); # create new line variable to return later
  xyz = [0, 0, 0]; # init xyz array to store xyz vals [x, y, z]
  for i, code in enumerate(line):
    if len(code) > 0:
      axis = code[0] # determine x, y, or z axis
      # depending on axis, store numeric values in different locations in xyz
      if axis == "x" or axis == "X": xyz[0] = code[1:]
      elif axis == "y" or axis == "Y": xyz[1] = code[1:]
      elif axis == "z" or axis == "Z": 
        # Z will always be the last axis so rewrite values into new_line once
        # we finish transforming the Z code
        xyz[2] = code[1:]
        xyz_transformed = transform_xyz(xyz);
        # rewrite current line transformed into new_line variable
        for j, code_ in enumerate(line):
          axis_ = code_[0]
          new_line[j] = code_;
          if axis_ == "x" or axis_ == "X": new_line[j] = "X" + str(xyz_transformed[0])
          elif axis_ == "y" or axis_ == "Y": new_line[j] = "Y" + str(xyz_transformed[1])
          elif axis_ == "z" or axis_ == "Z": new_line[j] = "Z" + str(xyz_transformed[2])
      else:
        new_line[i] = code;
  return " ".join(new_line); # join each element in new_line with a " "

# transform gcode file at path
def transform(path):
  gcode = read_f(path); # gcode file as string
  lines = gcode.splitlines(); # split gcode file up by newlines
  new_lines = [[]]*len(lines) # new_lines variable to store transformed gcode
  print("\nParsing and transforming gcode lines...");
  for i, line in enumerate(lines):
    new_line = parse_line(line); # parse and transform each line
    new_lines[i] = new_line; # write transformed line into new_lines
  print("%d lines of gcode parsed and transformed." % (len(new_lines)))
  new_gcode = "\n".join(new_lines) # join transformed lines of gcode with newline
  write_transform(path, new_gcode) # write new gcode to path (non-destructive)
        
if __name__ == "__main__":
  args = sys.argv
  if len(args) < 2: transform('smiley.gcode')
  else: transform(args[1])