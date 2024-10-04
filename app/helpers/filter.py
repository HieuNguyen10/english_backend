from fastapi import Request
from urllib.parse import urlsplit, parse_qs
def getFilter(request: Request):
    try:
        q_params = parse_qs(request.url.query, keep_blank_values=True)    
        d = dict((k, v if len(v)>1 else v[0]) 
                for k, v in q_params.items())
        arr = []
        for x, y in d.items():
            val = x.split("__")
            if(len(val) > 1):
                print(x.split("__")[0])
                print(x.split("__")[1])
                arr.append((x.split("__")[0], x.split("__")[1], y))
        return arr
    except Exception as exc:
        print(exc)
        pass
    
def getByCodeMax(model, sku):
    def getNextId(context):
        sql = """
            SELECT MAX(id)
            FROM %s
            """ % (model, )
        result = context.connection.execute(sql).fetchone()
        if result[0] is not None:
            next_id = result[0] + 1
        else:
            next_id = 1
        formatted_id = str(next_id).zfill(4)  # Đảm bảo số có độ dài 4 ký tự
        return sku + formatted_id
    return getNextId