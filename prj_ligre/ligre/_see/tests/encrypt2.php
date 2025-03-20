#!/bin/env php
<?php
function encrypt($key, $plaintext) {
    $iv = random_bytes(16); // Gera um IV de 16 bytes
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


exit;

# /opt/shared/evoice/py/tests/encrypt.php

// $c = new Crypt;
$message = 'SSss!#Mais1234';
// $encrypted = $c->encrypt($message);
// $decrypted = $c->decrypt($encrypted);

// print "Message..: {$message}\n";
// print "Encrypted: {$encrypted}\n";
// print "Decrypted: {$decrypted}\n";

class Crypt {
	protected $key = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa';
	protected $iv = '11111111111aaaaaaaa1111111111111';
	protected $cipher = 'AES-256-CBC';
	public function __construct(string $key = null, string $iv = null, string $cipher = null) {
		$l = $this->cipherLen($cipher);
		$this->cipher = $l['cipher'];
		print_r($l);
		$this->iv = substr($iv ? $iv : $this->iv, $l['iv']);
		$this->key = substr($key ? $key : $this->key, $l['key']);
	}
	public function cipherLen($cipher = null) {
		if ($cipher) {
			$cipher = strtoupper($cipher);
			$cipher_methods = openssl_get_cipher_methods();
			if (!in_array($cipher, $cipher_methods)) $cipher = $this->cipher;
		} else $cipher = $this->cipher;
		$iv_length = openssl_cipher_iv_length($cipher);
		$key = openssl_random_pseudo_bytes($iv_length * 2);
		return [
			'cipher' => $cipher,
			'iv' => $iv_length,
			'key' => strlen($key),
		];
	}
	public function encrypt($content) {
		$content = openssl_encrypt($content, $this->cipher, $this->key, 0, $this->iv);
		$content = base64_encode($content);
		return $content;
	}
	
	public function decrypt($content) {
		$content = base64_decode($content);
		$content = openssl_decrypt($content, $this->cipher, $this->key, 0, $this->iv);
		return $content;
	}
}

require_once '/opt/shared/evoice/vendor/phpseclib/phpseclib/phpseclib/Crypt/AES.php';
require_once '/opt/shared/evoice/vendor/phpseclib/phpseclib/phpseclib/Crypt/Hash.php';
require_once '/opt/shared/evoice/vendor/phpseclib/phpseclib/phpseclib/Math/BigInteger.php';

function get_key_and_iv($password, $salt, $klen = 32, $ilen = 16, $msgdgst = 'sha256') {
    $mdf = new Crypt_Hash($msgdgst);
    $password = utf8_encode($password);
    $salt = hex2bin($salt);

    try {
        $maxlen = $klen + $ilen;
        $keyiv = $mdf->hash($password . $salt);
        $tmp = [$keyiv];
        while (strlen(implode($tmp)) < $maxlen) {
            $tmp[] = $mdf->hash(end($tmp) . $password . $salt);
            $keyiv .= end($tmp);
        }
        $key = substr($keyiv, 0, $klen);
        $iv = substr($keyiv, $klen, $ilen);
        return [$key, $iv];
    } catch (Exception $e) {
        return [null, null];
    }
}

function encrypt($plaintext, $key, $mode, $salt) {
    list($key, $iv) = get_key_and_iv($key, $salt);
    $cipher = new Crypt_AES($mode);
    $cipher->setKey($key);
    $cipher->setIV($iv);
    return $cipher->encrypt($plaintext);
}

function decrypt($ciphertext, $key, $mode, $salt) {
    list($key, $iv) = get_key_and_iv($key, $salt);
    $cipher = new Crypt_AES($mode);
    $cipher->setKey($key);
    $cipher->setIV($iv);
    return $cipher->decrypt($ciphertext);
}

function append_padding($data, $block_size = 16) {
    $pad = $block_size - (strlen($data) % $block_size);
    return $data . str_repeat(chr($pad), $pad);
}

function remove_padding($data, $block_size = 16) {
    $pad = ord($data[strlen($data) - 1]);
    return substr($data, 0, -$pad);
}

$message = 'SSss!#Mais1234';
$plaintext = $message;
$key = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa';
$salt = '241fa86763b85341';

// Para usar a entrada de linha de comando (semelhante ao sys.argv em Python)
if ($argc > 1) {
    $plaintext = $argv[1];
}
if ($argc > 2) {
    $key = $argv[2];
}
if ($argc > 3) {
    $salt = $argv[3];
}

echo "Plaintext.: $plaintext\n";
echo "Passphrase: $key\n";
echo "Salt......: $salt\n";

// Adiciona padding (CMS padding não é uma função padrão do PHP, então adaptamos para padding padrão de AES)
$plaintext = append_padding($plaintext);

list($ciphertext, $ctext) = encrypt($plaintext, $key, Crypt_AES::MODE_CBC, $salt);
$ctext = 'Salted__' . hex2bin($salt) . $ciphertext;

$bd = base64_encode($ctext);
echo "Cipher (CBC) - Base64: $bd\n";
echo "Cipher (CBC) - Hex: " . bin2hex($ctext) . "\n";
echo "Cipher in binary: " . $ctext . "\n";

$decrypted = decrypt($ciphertext, $key, Crypt_AES::MODE_CBC, $salt);
$decrypted = remove_padding($decrypted);
echo "Decrypted: $decrypted\n";

