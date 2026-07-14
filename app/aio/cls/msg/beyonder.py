from app.aio.cls.msg.base import Templates, BaseText

class BeyonderText(BaseText):
    drink_template = Templates(templates_file_name='drink.txt')
    upseq_template = Templates(templates_file_name='drink.txt')
    downseq_template = Templates(templates_file_name='downseq.txt')
    kill_template = Templates(templates_file_name='kill.txt')
  
    @property
    def drink(self):
        return self.drink_template.random().format_map(self.data.model_dump())

    @property
    def upseq(self):
        return self.upseq_template.random().format_map(self.data.model_dump())
    
    @property
    def downseq(self):
        return self.downseq_template.random().format_map(self.data.model_dump())
    
    @property
    def kill(self):
        return self.kill_template.random().format_map(self.data.model_dump())
    