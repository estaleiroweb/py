#!/bin/bash

encrypt() {
  local key=$1
  local plaintext=$2
  local iv=$(openssl rand -base64 12) # Gera um IV de 16 bytes e codifica em base64
  local encrypted=$(echo -n "$plaintext" | openssl enc -aes-256-cbc -base64 -K $(echo -n "$key" | xxd -p) -iv $(echo "$iv" | base64 --decode | xxd -p))
  echo "$iv:$encrypted"
}

decrypt() {
  local key=$1
  local iv_encrypted=$2
  local iv=$(echo "$iv_encrypted" | cut -d':' -f1)
  local encrypted=$(echo "$iv_encrypted" | cut -d':' -f2)
  echo "$encrypted" | openssl enc -aes-256-cbc -d -base64 -K $(echo -n "$key" | xxd -p) -iv $(echo "$iv" | base64 --decode | xxd -p)
}

# Exemplo de uso
key="12345678901234567890123456789012"  # Chave de 32 bytes
plaintext="Mensagem secreta"

echo "Texto original: $plaintext"

encrypted=$(encrypt "$key" "$plaintext")
echo "Criptografado: $encrypted"

decrypted=$(decrypt "$key" "$encrypted")
echo "Descriptografado: $decrypted"
