#!/usr/bin/env python3
"""
Git 커밋 메시지 변환 및 검증 스킬

Git 커밋 메시지를 다양한 컨벤션으로 변환하고 규칙 준수 여부를 검증합니다.
"""

import os
import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Tuple
import anthropic


class ConventionType(Enum):
    """커밋 메시지 컨벤션 타입"""
    CONVENTIONAL = "conventional"
    GITMOJI = "gitmoji"
    ANGULAR = "angular"
    SEMANTIC = "semantic"


@dataclass
class ValidationRule:
    """커밋 메시지 검증 규칙"""
    convention: ConventionType
    max_length: int = 72
    require_scope: bool = False
    require_body: bool = False
    allowed_types: Optional[List[str]] = None
    custom_pattern: Optional[str] = None


@dataclass
class TransformRequest:
    """커밋 메시지 변환 요청"""
    message: str
    source_convention: Optional[ConventionType] = None
    target_convention: ConventionType = ConventionType.CONVENTIONAL
    preserve_body: bool = True
    language: str = "en"


@dataclass
class ValidationResult:
    """검증 결과"""
    is_valid: bool
    errors: List[str]
    suggestions: List[str]
    corrected_message: Optional[str] = None


class GitCommitMessageSkill:
    """Git 커밋 메시지 변환 및 검증 스킬"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        초기화
        
        Args:
            api_key: Anthropic API 키 (None이면 환경변수에서 로드)
        """
        self.client = anthropic.Anthropic(
            api_key=api_key or os.environ.get("ANTHROPIC_API_KEY")
        )
        self.model = "claude-3-5-sonnet-20241022"
    
    def transform_message(self, request: TransformRequest) -> str:
        """
        커밋 메시지를 지정된 컨벤션으로 변환
        
        Args:
            request: 변환 요청 정보
            
        Returns:
            변환된 커밋 메시지
        """
        source_info = f"Source convention: {request.source_convention.value}" if request.source_convention else "Auto-detect convention"
        
        prompt = f"""Transform the following Git commit message to {request.target_convention.value} convention.

{source_info}
Target convention: {request.target_convention.value}
Target language: {request.language}
Preserve body: {request.preserve_body}

Original message:
{request.message}

Requirements:
- Follow {request.target_convention.value} convention strictly
- Output language: {request.language}
- {'Keep the commit body if present' if request.preserve_body else 'Keep only the subject line'}
- Subject line should be concise and clear

For conventions:
- conventional: type(scope): description
- gitmoji: :emoji: description
- angular: type(scope): description (types: build, ci, docs, feat, fix, perf, refactor, test)
- semantic: [MAJOR|MINOR|PATCH] description

Output ONLY the transformed commit message, nothing else."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return message.content[0].text.strip()
        except Exception as e:
            raise RuntimeError(f"Failed to transform message: {str(e)}")
    
    def validate_message(self, message: str, rule: ValidationRule) -> ValidationResult:
        """
        커밋 메시지가 규칙을 준수하는지 검증
        
        Args:
            message: 검증할 커밋 메시지
            rule: 검증 규칙
            
        Returns:
            검증 결과
        """
        errors = []
        suggestions = []
        
        lines = message.split('\n')
        subject = lines[0] if lines else ""
        body = '\n'.join(lines[2:]) if len(lines) > 2 else ""
        
        # 길이 검증
        if len(subject) > rule.max_length:
            errors.append(f"Subject line exceeds {rule.max_length} characters (current: {len(subject)})")
            suggestions.append(f"Shorten the subject line to {rule.max_length} characters or less")
        
        # 본문 필수 검증
        if rule.require_body and not body.strip():
            errors.append("Commit body is required but missing")
            suggestions.append("Add a detailed commit body explaining the changes")
        
        # 컨벤션별 검증
        if rule.convention == ConventionType.CONVENTIONAL:
            errors_conv, suggestions_conv = self._validate_conventional(subject, rule)
            errors.extend(errors_conv)
            suggestions.extend(suggestions_conv)
        elif rule.convention == ConventionType.GITMOJI:
            errors_conv, suggestions_conv = self._validate_gitmoji(subject)
            errors.extend(errors_conv)
            suggestions.extend(suggestions_conv)
        elif rule.convention == ConventionType.ANGULAR:
            errors_conv, suggestions_conv = self._validate_angular(subject, rule)
            errors.extend(errors_conv)
            suggestions.extend(suggestions_conv)
        
        # 커스텀 패턴 검증
        if rule.custom_pattern and not re.match(rule.custom_pattern, subject):
            errors.append(f"Subject does not match custom pattern: {rule.custom_pattern}")
            suggestions.append("Adjust the commit message to match the required pattern")
        
        # 오류가 있으면 수정된 메시지 생성
        corrected_message = None
        if errors:
            corrected_message = self._generate_corrected_message(message, rule, errors)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            suggestions=suggestions,
            corrected_message=corrected_message
        )
    
    def _validate_conventional(self, subject: str, rule: ValidationRule) -> Tuple[List[str], List[str]]:
        """Conventional Commits 형식 검증"""
        errors = []
        suggestions = []
        
        pattern = r'^(\w+)(\([^)]+\))?!?:\s.+'
        match = re.match(pattern, subject)
        
        if not match:
            errors.append("Does not follow Conventional Commits format (type(scope): description)")
            suggestions.append("Use format: type(scope): description (e.g., feat(auth): add login feature)")
            return errors, suggestions
        
        commit_type = match.group(1)
        has_scope = match.group(2) is not None
        
        if rule.allowed_types and commit_type not in rule.allowed_types:
            errors.append(f"Type '{commit_type}' not in allowed types: {', '.join(rule.allowed_types)}")
            suggestions.append(f"Use one of: {', '.join(rule.allowed_types)}")
        
        if rule.require_scope and not has_scope:
            errors.append("Scope is required but missing")
            suggestions.append("Add scope in parentheses: type(scope): description")
        
        return errors, suggestions
    
    def _validate_gitmoji(self, subject: str) -> Tuple[List[str], List[str]]:
        """Gitmoji 형식 검증"""
        errors = []
        suggestions = []
        
        if not re.match(r'^:[a-z_]+:\s.+', subject):
            errors.append("Does not follow Gitmoji format (:emoji: description)")
            suggestions.append("Use format: :emoji: description (e.g., :sparkles: add new feature)")
        
        return errors, suggestions
    
    def _validate_angular(self, subject: str, rule: ValidationRule) -> Tuple[List[str], List[str]]:
        """Angular 커밋 컨벤션 검증"""
        errors = []
        suggestions = []
        
        angular_types = ['build', 'ci', 'docs', 'feat', 'fix', 'perf', 'refactor', 'test']
        allowed = rule.allowed_types or angular_types
        
        pattern = r'^(\w+)(\([^)]+\))?:\s.+'
        match = re.match(pattern, subject)
        
        if not match:
            errors.append("Does not follow Angular commit format")
            suggestions.append(f"Use format: type(scope): description with types: {', '.join(allowed)}")
            return errors, suggestions
        
        commit_type = match.group(1)
        if commit_type not in allowed:
            errors.append(f"Type '{commit_type}' not in Angular types: {', '.join(allowed)}")
            suggestions.append(f"Use one of: {', '.join(allowed)}")
        
        return errors, suggestions
    
    def _generate_corrected_message(self, message: str, rule: ValidationRule, errors: List[str]) -> str:
        """오류를 수정한 메시지 생성"""
        prompt = f"""Correct the following Git commit message to comply with {rule.convention.value} convention.

Original message:
{message}

Validation errors found:
{chr(10).join(f'- {error}' for error in errors)}

Requirements:
- Convention: {rule.convention.value}
- Max subject length: {rule.max_length}
- Scope required: {rule.require_scope}
- Body required: {rule.require_body}
{f'- Allowed types: {", ".join(rule.allowed_types)}' if rule.allowed_types else ''}

Output ONLY the corrected commit message, nothing else."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text.strip()
        except Exception as e:
            return f"Error generating correction: {str(e)}"
    
    def batch_transform(self, messages: List[str], target_convention: ConventionType, language: str = "en") -> List[str]:
        """
        여러 커밋 메시지를 일괄 변환
        
        Args:
            messages: 변환할 커밋 메시지 리스트
            target_convention: 대상 컨벤션
            language: 출력 언어
            
        Returns:
            변환된 커밋 메시지 리스트
        """
        results = []
        for msg in messages:
            request = TransformRequest(
                message=msg,
                target_convention=target_convention,
                language=language
            )
            try:
                transformed = self.transform_message(request)
                results.append(transformed)
            except Exception as e:
                results.append(f"ERROR: {str(e)}")
        
        return results
    
    def batch_validate(self, messages: List[str], rule: ValidationRule) -> List[ValidationResult]:
        """
        여러 커밋 메시지를 일괄 검증
        
        Args:
            messages: 검증할 커밋 메시지 리스트
            rule: 검증 규칙
            
        Returns:
            검증 결과 리스트
        """
        return [self.validate_message(msg, rule) for msg in messages]


def main():
    """메인 실행 함수"""
    print("=== Git 커밋 메시지 변환 및 검증 스킬 ===\n")
    
    # 스킬 인스턴스 생성
    skill = GitCommitMessageSkill()
    
    # 예제 1: 커밋 메시지 변환
    print("[ 예제 1: Conventional Commits로 변환 ]")
    original_message = "added user authentication feature with JWT tokens"
    request = TransformRequest(
        message=original_message,
        target_convention=ConventionType.CONVENTIONAL,
        language="en"
    )
    
    print(f"원본 메시지: {original_message}")
    transformed = skill.transform_message(request)
    print(f"변환된 메시지: {transformed}\n")
    
    # 예제 2: Gitmoji로 변환
    print("[ 예제 2: Gitmoji로 변환 ]")
    request_gitmoji = TransformRequest(
        message="fix: resolve memory leak in cache manager",
        target_convention=ConventionType.GITMOJI,
        language="en"
    )
    
    print(f"원본 메시지: {request_gitmoji.message}")
    transformed_gitmoji = skill.transform_message(request_gitmoji)
    print(f"변환된 메시지: {transformed_gitmoji}\n")
    
    # 예제 3: 커밋 메시지 검증
    print("[ 예제 3: Conventional Commits 규칙 검증 ]")
    test_messages = [
        "feat(auth): add OAuth2 login support",
        "fixed bug",  # 잘못된 형식
        "docs: update README with installation instructions that are very very very very long and exceed the maximum length",  # 너무 긴 메시지
    ]
    
    rule = ValidationRule(
        convention=ConventionType.CONVENTIONAL,
        max_length=72,
        require_scope=False,
        allowed_types=["feat", "fix", "docs", "style", "refactor", "test", "chore"]
    )
    
    for i, msg in enumerate(test_messages, 1):
        print(f"\n메시지 {i}: {msg}")
        result = skill.validate_message(msg, rule)
        
        if result.is_valid:
            print("✓ 검증 통과")
        else:
            print("✗ 검증 실패")
            print(f"  오류: {', '.join(result.errors)}")
            print(f"  제안: {', '.join(result.suggestions)}")
            if result.corrected_message:
                print(f"  수정된 메시지: {result.corrected_message}")
    
    # 예제 4: 일괄 변환
    print("\n\n[ 예제 4: 여러 메시지 일괄 변환 ]")
    legacy_messages = [
        "update documentation",
        "fix authentication bug",
        "add new API endpoint"
    ]
    
    print("레거시 메시지:")
    for msg in legacy_messages:
        print(f"  - {msg}")
    
    print("\nConventional Commits로 변환 중...")
    transformed_batch = skill.batch_transform(
        legacy_messages,
        ConventionType.CONVENTIONAL,
        language="en"
    )
    
    print("\n변환 결과:")
    for original, transformed in zip(legacy_messages, transformed_batch):
        print(f"  {original}")
        print(f"  → {transformed}\n")
    
    print("\n=== 실행 완료 ===")


if __name__ == "__main__":
    main()