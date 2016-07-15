def resolve_modified_val(base_val, *modifiers):
    mul_div_ops = [mod for mod in modifiers if mod.op in ["*","/"] ]
    add_sub_ops = [mod for mod in modifiers if mod.op in ["+", "-"] ]
    res = base_val
    for mod in mul_div_ops:
        res = mod.get_modified_val(res)
    for mod in add_sub_ops:
        res = mod.get_modified_val(res)
    return res
