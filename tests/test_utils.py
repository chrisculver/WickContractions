import src.wick_utilities as utils

def test_perms():
  assert sorted([[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]) == sorted([[i for i in lst] for lst in utils.permutations([1,2,3])])

  assert utils.arePermsEqualParity([1,2,3],[1,3,2])==False
  assert utils.arePermsEqualParity([1,2,3],[3,1,2])==True
