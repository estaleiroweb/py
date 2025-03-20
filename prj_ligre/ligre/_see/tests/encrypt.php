#!/bin/env php
<?php
function encrypt($key, $plaintext) {
    $iv = openssl_random_pseudo_bytes(16); // Gera um IV de 16 bytes
    $ciphertext = openssl_encrypt($plaintext, 'AES-256-CBC', $key, OPENSSL_RAW_DATA, $iv);
    return base64_encode($iv . $ciphertext);
}

function decrypt($key, $b64_ciphertext) {
    $data = base64_decode($b64_ciphertext);
    $iv = substr($data, 0, 16);
    $ciphertext = substr($data, 16);
    return openssl_decrypt($ciphertext, 'AES-256-CBC', $key, OPENSSL_RAW_DATA, $iv);
}

// Exemplo de uso
$key = "12345678901234567890123456789012";  // Chave de 32 bytes
$plaintext = "Mensagem secreta";

$encrypted = encrypt($key, $plaintext);
echo "Criptografado: $encrypted\n";

$decrypted = decrypt($key, $encrypted);
echo "Descriptografado: $decrypted\n";
?>
