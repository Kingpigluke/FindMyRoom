import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

import { APIService } from './api-service';

describe('APIService', () => {
  let service: APIService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [APIService]
    });
    service = TestBed.inject(APIService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should get all node from the API', () => {
    const mockNodes = [
      { id: 'A', name: 'Main entrance'},
      { id: 'B', name: 'Room 101'},
      { id: 'C', name: 'Crossroads'}
    ];

    service.getNodes().subscribe((nodes) => {
      expect(nodes).toEqual(mockNodes);
      expect(nodes).toHaveLength(3);
    });

    const req = httpMock.expectOne('http://localhost:5000/api/nodes');
    expect(req.request.method).toBe('GET');
    req.flush(mockNodes);
  });

  it('should return an Observable', () => {
    const result = service.getNodes();
    expect(result).toBeDefined();
    expect(result.subscribe).toBeDefined();
  })
});
