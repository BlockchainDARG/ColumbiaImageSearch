import os
import glob
import cPickle as pickle
from .generic_storer import GenericStorer
from ..common.dl import mkpath
from cufacesearch.common.error import full_trace_error

default_prefix = "LO_"

class LocalStorer(GenericStorer):

  def __init__(self, global_conf_in, prefix=default_prefix):
    super(LocalStorer, self).__init__(global_conf_in, prefix)
    self.base_path = self.get_required_param('base_path')
    # Be sure base_path ends by "/" for mkpath
    if self.base_path[-1] != "/":
      self.base_path = self.base_path+"/"
    self.setup()

  def set_pp(self):
    self.pp = "LocalStorer"

  def setup(self):
    # create base path dir
    mkpath(self.base_path)
    print "[{}: log] Initialized with base_path '{}'".format(self.pp, self.base_path)

  def get_full_path(self, key):
    return os.path.join(self.base_path, key)

  def save(self, key, obj):
    # Pickle and save to disk
    full_path = self.get_full_path(key)
    mkpath(full_path)
    pickle.dump(obj, open(full_path, 'wb'))

  def load(self, key):
    # Load a pickle object from disk
    try:
      full_path = self.get_full_path(key)
      obj = pickle.load(open(full_path, 'rb'))
      return obj
    except Exception as e:
      err_msg = "[{}: error ({}: {})] Could not load object from path: {}"
      print err_msg.format(self.pp, type(e), e, full_path)


  def list_prefix(self, prefix_path):
    for filepath in glob.glob(self.get_full_path(prefix_path)+"*"):
      yield filepath

  # This would be used to load all codes
  def get_all_from_prefix(self, prefix_path):
    for filepath in self.list_prefix(prefix_path):
      obj = self.load(filepath)
      if obj:
        yield obj

if __name__ == "__main__":
  local_conf = {"base_path": "./store/"}
  lst = LocalStorer(local_conf, prefix="")