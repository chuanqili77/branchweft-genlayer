"""Real pinned SDK/storage with mocked LLM. Not network consensus."""
import json
from pathlib import Path
from gltest.direct import VMContext,deploy_contract
root=Path(__file__).resolve().parents[1];units=json.loads((root/'examples/document.json').read_text());owner='0x'+'1'*40
vectors=[('CHANGE','EQ','CHANGE'),('EQ','CHANGE','CHANGE'),('EQ','EQ','EQ')]
answer={'units':[{'id':u['id'],'base_left':v[0],'base_right':v[1],'left_right':v[2],'reason':'The snapshots preserve or materially change the stated terms.'} for u,v in zip(units,vectors)]}
vm=VMContext();vm.sender=owner;vm.mock_llm('^Compare three fixed',json.dumps(answer))
with vm.activate():
 c=deploy_contract(root/'contracts/branch_weft.py',vm,sdk_version='v0.3.0-rc7');c.stage('sdk',json.dumps(units));r=json.loads(c.merge(owner,'sdk'))
 assert [x['source'] for x in r['result']['choices']]==['left','right','base'];assert vm.run_validator() is True
 vm.clear_mocks();answer['units'][0]['base_left']='EQ';vm.mock_llm('^Compare three fixed',json.dumps(answer));assert vm.run_validator() is False
 c.publish(owner,'sdk',r['result_digest']);assert json.loads(c.get_document(owner,'sdk'))['status']=='PUBLISHED'
print('PASS: SDK storage/calldata, source selection, independent validator accept/reject and publication (mocked LLM).')
