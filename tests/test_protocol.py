"""Actual contract source with mocked host/model; no live semantic accuracy claim."""
import importlib.util,itertools,json,sys,types,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A='0x'+'1'*40;B='0x'+'2'*40
class Return:
 def __init__(self,x):self.calldata=x
class Public:
 write=staticmethod(lambda f:f);view=staticmethod(lambda f:f)
gl=types.SimpleNamespace(Contract=object,public=Public(),message=types.SimpleNamespace(sender_address=A),vm=types.SimpleNamespace(Return=Return,UserError=ValueError),nondet=types.SimpleNamespace())
sys.modules['genlayer']=types.SimpleNamespace(gl=gl,TreeMap=dict)
spec=importlib.util.spec_from_file_location('b',ROOT/'contracts/branch_weft.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
UNITS=json.loads((ROOT/'examples/document.json').read_text())
def result(vectors=None):
 vectors=vectors or [('CHANGE','EQ','CHANGE'),('EQ','CHANGE','CHANGE'),('EQ','EQ','EQ')]
 return {'units':[{'id':'U'+str(i+1),'base_left':v[0],'base_right':v[1],'left_right':v[2],'reason':'The snapshots make the stated material changes to these terms.'} for i,v in enumerate(vectors)]}
class Tests(unittest.TestCase):
 def setUp(self):
  gl.message.sender_address=A;self.c=b.BranchWeft();self.answer=result();self.second=None;self.calls=0
  def llm(*a,**kw):self.calls+=1;return self.second if self.calls>1 and self.second else self.answer
  gl.nondet.exec_prompt=llm
  def run(l,v):
   x=l()
   if not v(Return(x)):raise ValueError('DISAGREE')
   return x
  gl.vm.run_nondet_unsafe=run
 def stage(self):return self.c.stage('notice',json.dumps(UNITS))
 def merge(self):return json.loads(self.c.merge(A,'notice'))
 def test_source_selecting_lifecycle(self):
  self.stage();r=self.merge();self.assertEqual([x['source'] for x in r['result']['choices']],['left','right','base'])
  r=json.loads(self.c.publish(A,'notice',r['result_digest']));self.assertEqual(r['status'],'PUBLISHED')
 def test_no_fabricated_output(self):
  self.stage();r=self.merge()
  for i,x in enumerate(r['result']['choices']):self.assertEqual(x['text'],UNITS[i][x['source']])
 def test_digest_guard(self):
  self.stage();self.merge()
  with self.assertRaisesRegex(ValueError,'DIGEST_MISMATCH'):self.c.publish(A,'notice','wrong')
 def test_owner_only(self):
  self.stage();gl.message.sender_address=B
  with self.assertRaisesRegex(ValueError,'NOT_OWNER'):self.merge()
 def test_immutable_input(self):
  self.stage()
  with self.assertRaisesRegex(ValueError,'ID_USED'):self.stage()
 def test_no_remerge_or_republish(self):
  self.stage();r=self.merge()
  with self.assertRaisesRegex(ValueError,'ALREADY_MERGED'):self.merge()
  self.c.publish(A,'notice',r['result_digest'])
  with self.assertRaisesRegex(ValueError,'NOT_PUBLISHABLE'):self.c.publish(A,'notice',r['result_digest'])
 def test_independent_disagreement_atomic(self):
  self.stage();self.second=result([('EQ','EQ','EQ')]*3)
  with self.assertRaisesRegex(ValueError,'DISAGREE'):self.merge()
  self.assertEqual(json.loads(self.c.get_document(A,'notice'))['status'],'STAGED')
 def test_exact_text_cannot_be_misclassified(self):
  raw=result();raw['units'][0]['base_right']='CHANGE'
  with self.assertRaisesRegex(ValueError,'EXACT_TEXT_MUST_MATCH'):b.findings(raw,UNITS)
 def test_conflict_and_unknown_block_publication(self):
  for labels in [('CHANGE','CHANGE','CHANGE'),('UNKNOWN','CHANGE','CHANGE')]:
   r=b.select(UNITS,result([labels]*3)['units']);self.assertIn(r['status'],['CONFLICT','REVIEW']);self.assertEqual(r['merged_text'],'')
 def test_triangle_inconsistency(self):
  r=b.select(UNITS,result([('EQ','EQ','CHANGE')]*3)['units']);self.assertEqual(r['status'],'REVIEW')
 def test_same_new_meaning_prefers_left_bytes(self):
  r=b.select(UNITS,result([('CHANGE','CHANGE','EQ')]*3)['units']);self.assertEqual([x['source'] for x in r['choices']],['left']*3)
 def test_all_label_triples(self):
  for v in itertools.product(['EQ','CHANGE','UNKNOWN'],repeat=3):
   r=b.select(UNITS,result([v]*3)['units'])
   if 'UNKNOWN' in v or v.count('EQ')==2:expected='REVIEW'
   elif v==('CHANGE','CHANGE','CHANGE'):expected='CONFLICT'
   else:expected='MERGED'
   self.assertEqual(r['status'],expected)
 def test_malformed_or_reordered(self):
  for raw in [{'units':[]},{'units':list(reversed(result()['units']))}]:
   with self.assertRaises(ValueError):b.findings(raw,UNITS)
if __name__=='__main__':unittest.main()
