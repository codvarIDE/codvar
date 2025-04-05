import re

def convert_html_to_react_native(html_content):
 
    html_content = re.sub(r'<!DOCTYPE[^>]*>', '', html_content)
    html_content = re.sub(r'<html[^>]*>|</html>', '', html_content)
    html_content = re.sub(r'<head[^>]*>.*?</head>', '', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<body[^>]*>|</body>', '', html_content)
 
    tag_mappings = {
        r'<div([^>]*)>': r'<View\1>',
        r'</div>': '</View>',
        r'<p([^>]*)>': r'<Text\1>',
        r'</p>': '</Text>',
        r'<span([^>]*)>': r'<Text\1>',
        r'</span>': '</Text>',
        r'<img([^>]*?)src="([^"]*)"([^>]*)>': r'<Image\1source={{uri: "\2"}}\3>',
    }

    for html_tag, rn_component in tag_mappings.items():
        html_content = re.sub(html_tag, rn_component, html_content)

    def convert_styles(match):
        style_str = match.group(1)
        styles = {}
        for style in style_str.split(';'):
            if ':' in style:
                prop, value = style.split(':')
              
                prop = prop.strip().replace('-', '')
                value = value.strip()
                if value.endswith('px'):
                    value = value[:-2] 
                styles[prop] = value
        style_obj = ', '.join(f'{k}: "{v}"' for k, v in styles.items())
        return f'style={{ {{{style_obj}}} }}'

    html_content = re.sub(r'style="([^"]*)"', convert_styles, html_content)

    
    react_native_code = """import React from 'react';
import { View, Text, Image, StyleSheet } from 'react-native';

const App = () => {
  return (
    <View style={styles.container}>
"""
    react_native_code += f"      {html_content}\n"
    react_native_code += """    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
  },
});

export default App;
"""
    return react_native_code


if __name__ == "__main__":
     
    with open('index.html', 'r') as file:
        sample_html = file.read()
    
    result = convert_html_to_react_native(sample_html)
    print(result)
