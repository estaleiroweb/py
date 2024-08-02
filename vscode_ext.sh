#!/bin/bash

# Função para obter os detalhes de uma extensão
get_extension_details() {
	extension_name="$1"
	response=$(curl -s -X POST https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery \
		-H "Content-Type: application/json" \
		-H "Accept: application/json;api-version=3.0-preview.1" \
		-d "{
      \"filters\": [{
        \"criteria\": [{
          \"filterType\": 7,
          \"value\": \"$extension_name\"
        }]
      }],
      \"flags\": 103
    }")

	echo "$response" | jq -r --arg name "$extension_name" '
    .results[0].extensions[0] | 
    {
      name: .displayName,
      author: .publisher.displayName,
      description: .shortDescription,
      image: (.versions[0].files[] | select(.assetType == "Microsoft.VisualStudio.Services.Icons.Default").source),
      link: "https://marketplace.visualstudio.com/items?itemName=\(.publisher.publisherName).\($name)"
    }
  '
}

# Obtém a lista de extensões instaladas
extensions=$(code --list-extensions)

# Itera sobre cada extensão e exibe os detalhes no formato desejado
for ext in $extensions; do
	details=$(get_extension_details "$ext")
	name=$(echo "$details" | jq -r '.name')
	author=$(echo "$details" | jq -r '.author')
	description=$(echo "$details" | jq -r '.description')
	image=$(echo "$details" | jq -r '.image')
	link=$(echo "$details" | jq -r '.link')

	if [ ! "$name" ]; then
		name='Nome'
		author='author'
		description='description'
		image='image'
		link='link'
	fi
	# Exibe a saída formatada em Markdown
	echo "[<img src='$image' /> $name]($link): ($ext) Autor: $author<pre>"
	echo $description
	echo "</pre>"
	echo
	echo
done
