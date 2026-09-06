import { describe, it, expect } from 'bun:test';
import {
  LoginType,
  LoginTypeLabel,
  OperationType,
  getApprovalCount,
} from '../../lib/types';

describe('lib/types', () => {
  describe('LoginType enum', () => {
    it('should have correct values', () => {
      expect(LoginType.Email).toBe(0);
      expect(LoginType.Phone).toBe(1);
      expect(LoginType.Google).toBe(2);
      expect(LoginType.Apple).toBe(3);
      expect(LoginType.Telegram).toBe(4);
      expect(LoginType.Twitter).toBe(5);
      expect(LoginType.Facebook).toBe(6);
    });
  });

  describe('LoginTypeLabel', () => {
    it('should map LoginType to readable labels', () => {
      expect(LoginTypeLabel[LoginType.Email]).toBe('Email');
      expect(LoginTypeLabel[LoginType.Phone]).toBe('Phone');
      expect(LoginTypeLabel[LoginType.Google]).toBe('Google');
      expect(LoginTypeLabel[LoginType.Apple]).toBe('Apple');
      expect(LoginTypeLabel[LoginType.Telegram]).toBe('Telegram');
    });
  });

  describe('OperationType enum', () => {
    it('should match on-chain caimpl.OperationType values', () => {
      expect(OperationType.Unknown).toBe(0);
      expect(OperationType.CreateCAHolder).toBe(1);
      expect(OperationType.SocialRecovery).toBe(2);
      expect(OperationType.AddGuardian).toBe(3);
      expect(OperationType.RemoveGuardian).toBe(4);
      expect(OperationType.UpdateGuardian).toBe(5);
      expect(OperationType.SetLoginAccount).toBe(7);
      expect(OperationType.Approve).toBe(8);
      expect(OperationType.ModifyTransferLimit).toBe(9);
      expect(OperationType.GuardianApproveTransfer).toBe(10);
    });

    it('should use CreateCAHolder(1) for registration and SocialRecovery(2) for login', () => {
      // Registration verification: operationType = 1 (CreateCAHolder)
      // Recovery/Login verification: operationType = 2 (SocialRecovery)
      expect(OperationType.CreateCAHolder).toBe(1);
      expect(OperationType.SocialRecovery).toBe(2);
      expect(OperationType.CreateCAHolder).not.toBe(OperationType.SocialRecovery);
    });
  });

  describe('getApprovalCount', () => {
    it('should require all guardians when count <= 3', () => {
      expect(getApprovalCount(1)).toBe(1);
      expect(getApprovalCount(2)).toBe(2);
      expect(getApprovalCount(3)).toBe(3);
    });

    it('should use floor(count * 3/5) + 1 when count > 3', () => {
      expect(getApprovalCount(4)).toBe(3); // floor(4*3/5) + 1 = floor(2.4) + 1 = 3
      expect(getApprovalCount(5)).toBe(4); // floor(5*3/5) + 1 = floor(3) + 1 = 4
      expect(getApprovalCount(6)).toBe(4); // floor(6*3/5) + 1 = floor(3.6) + 1 = 4
      expect(getApprovalCount(7)).toBe(5); // floor(7*3/5) + 1 = floor(4.2) + 1 = 5
      expect(getApprovalCount(10)).toBe(7); // floor(10*3/5) + 1 = floor(6) + 1 = 7
    });
  });
});
