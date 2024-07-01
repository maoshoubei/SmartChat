

def Call_Create_Repair_Wo_API(slot,scene_name,user_input):
    message = f'尊敬的XXX先生，您好！您的维修工单创建成功，工单编号为：R202406270001。工单信息如下：\n设备名称：{slot[0]["value"]}\n区域位置：{slot[1]["value"]}\n故障描述：{slot[2]["value"]}\n故障原因：{slot[3]["value"]}\n紧急程度：{slot[4]["value"]}'
    message += "\n您的维修工单已经为你下发成功，请注意工单流转状态~"
    return message
    
