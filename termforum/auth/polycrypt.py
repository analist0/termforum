"""PolyCrypt™ - Advanced Polynomial-based Password Hashing System

This module implements a custom password hashing algorithm combining:
- Polynomial rolling hash for unique fingerprinting
- PBKDF2 with SHA256 for cryptographic security
- Random salt generation (32 bytes)
- Configurable iteration count (default: 100,000)

Unlike standard bcrypt/scrypt, PolyCrypt adds a polynomial layer
for additional entropy and mathematical complexity.
"""

import hashlib
import secrets
import base64
from typing import Tuple


class PolyCrypt:
    """Advanced polynomial-based password hashing system"""

    # Configuration
    SALT_LENGTH = 32  # bytes
    ITERATIONS = 100000  # PBKDF2 iterations
    HASH_LENGTH = 64  # output hash length
    POLY_PRIME = 1000000007  # Large prime for polynomial hashing
    POLY_BASE = 31  # Base for polynomial computation

    @staticmethod
    def _polynomial_hash(text: str, salt: bytes) -> int:
        """
        Compute polynomial rolling hash for additional entropy

        Uses Rabin-Karp style polynomial:
        hash = (c[0] * base^(n-1) + c[1] * base^(n-2) + ... + c[n-1]) mod prime

        Args:
            text: Password string
            salt: Random salt bytes

        Returns:
            Integer hash value
        """
        result = 0
        combined = text.encode() + salt

        for i, byte in enumerate(combined):
            result = (result * PolyCrypt.POLY_BASE + byte) % PolyCrypt.POLY_PRIME

        return result

    @staticmethod
    def _generate_salt() -> bytes:
        """Generate cryptographically secure random salt"""
        return secrets.token_bytes(PolyCrypt.SALT_LENGTH)

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using PolyCrypt algorithm

        Process:
        1. Generate random salt
        2. Compute polynomial hash for entropy mixing
        3. Apply PBKDF2-SHA256 with polynomial hash as additional input
        4. Encode as base64 for storage

        Args:
            password: Plain text password

        Returns:
            Base64 encoded string: "salt$hash"
        """
        if not password:
            raise ValueError("Password cannot be empty")

        # Generate salt
        salt = PolyCrypt._generate_salt()

        # Compute polynomial hash
        poly_hash = PolyCrypt._polynomial_hash(password, salt)

        # Mix polynomial hash into password (additional entropy layer)
        enhanced_password = f"{password}:{poly_hash}".encode()

        # Apply PBKDF2 with SHA256
        key = hashlib.pbkdf2_hmac(
            'sha256',
            enhanced_password,
            salt,
            PolyCrypt.ITERATIONS,
            dklen=PolyCrypt.HASH_LENGTH
        )

        # Encode for storage: salt$hash
        salt_b64 = base64.b64encode(salt).decode('utf-8')
        hash_b64 = base64.b64encode(key).decode('utf-8')

        return f"{salt_b64}${hash_b64}"

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        Verify a password against a PolyCrypt hash

        Args:
            password: Plain text password to verify
            hashed: Stored hash from hash_password()

        Returns:
            True if password matches, False otherwise
        """
        if not password or not hashed:
            return False

        try:
            # Parse stored hash
            parts = hashed.split('$')
            if len(parts) != 2:
                return False

            salt_b64, stored_hash_b64 = parts
            salt = base64.b64decode(salt_b64)
            stored_hash = base64.b64decode(stored_hash_b64)

            # Recompute hash with same salt
            poly_hash = PolyCrypt._polynomial_hash(password, salt)
            enhanced_password = f"{password}:{poly_hash}".encode()

            computed_hash = hashlib.pbkdf2_hmac(
                'sha256',
                enhanced_password,
                salt,
                PolyCrypt.ITERATIONS,
                dklen=PolyCrypt.HASH_LENGTH
            )

            # Constant-time comparison to prevent timing attacks
            return secrets.compare_digest(computed_hash, stored_hash)

        except Exception:
            return False

    @staticmethod
    def check_password_strength(password: str) -> Tuple[int, str]:
        """
        Analyze password strength and return score + feedback

        Scoring:
        - Length: +10 per character (max 50)
        - Uppercase: +10
        - Lowercase: +10
        - Digits: +10
        - Special chars: +15
        - Entropy bonus: +5

        Args:
            password: Password to check

        Returns:
            Tuple of (score 0-100, strength_label)
        """
        if not password:
            return 0, "Empty"

        score = 0

        # Length score (max 50 points)
        score += min(len(password) * 10, 50)

        # Character variety
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        if has_upper:
            score += 10
        if has_lower:
            score += 10
        if has_digit:
            score += 10
        if has_special:
            score += 15

        # Entropy bonus (character set diversity)
        if sum([has_upper, has_lower, has_digit, has_special]) >= 3:
            score += 5

        # Cap at 100
        score = min(score, 100)

        # Determine strength label
        if score < 30:
            label = "Very Weak ❌"
        elif score < 50:
            label = "Weak ⚠️"
        elif score < 70:
            label = "Medium ⚡"
        elif score < 90:
            label = "Strong ✅"
        else:
            label = "Very Strong 🔒"

        return score, label


# Convenience functions
def hash_password(password: str) -> str:
    """Hash a password using PolyCrypt"""
    return PolyCrypt.hash_password(password)


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a PolyCrypt hash"""
    return PolyCrypt.verify_password(password, hashed)


def check_password_strength(password: str) -> Tuple[int, str]:
    """Check password strength"""
    return PolyCrypt.check_password_strength(password)
