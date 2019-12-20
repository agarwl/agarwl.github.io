{% extends 'basic.tpl'%}

{% block in_prompt %}
{% endblock in_prompt %}

{% block input %}
<d-code language="python">
{{ cell['source'] }}
</d-code>
{% endblock input %}