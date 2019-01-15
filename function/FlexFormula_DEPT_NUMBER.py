class DynamicFormulaInstance(BaseFormulaObject):
    def do(self, depart_id):
        depart_id = depart_id or self.context.get('CURRENT_DEPARTMENT')
        _ret = self.call_open_api('depart.card', {'id': depart_id})
        return "{}".format(_ret['data']['number'])
