import { TestBed } from '@angular/core/testing';

import { LexzigService } from './lexzig-service.service';

describe('LexzigServiceService', () => {
  let service: LexzigService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LexzigService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
