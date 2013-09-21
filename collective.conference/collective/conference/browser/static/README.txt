Use the static directory for non-template browser resources like images,
stylesheets and JavaScript.

Contents of this folder may be addressed in templates via view/static. For
example, if you placed at test.js resource in this folder, you could insert it
via template code like:


<head>
    <metal:block fill-slot="style_slot">
        <link rel="stylesheet" type="text/css"
            tal:define="navroot context/@@plone_portal_state/navigation_root_url"
            tal:attributes="href string:${navroot}/++resource++example.conference/conference.css"
            />
    </metal:block>
</head>
Static folder resources are public.