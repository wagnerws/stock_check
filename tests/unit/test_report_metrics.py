import pytest
from app.services.report_metrics import calculate_general_metrics, get_adjustment_items, get_state_distribution
import pandas as pd

def test_calculate_general_metrics_empty():
    total_base = 0
    scanned_items = []
    total_scanned, progress, pending = calculate_general_metrics(total_base, scanned_items)
    
    assert total_scanned == 0
    assert progress == 0.0
    assert pending == 0

def test_calculate_general_metrics_partial():
    total_base = 100
    scanned_items = [{'id': 1}, {'id': 2}, {'id': 3}] # 3 itens
    total_scanned, progress, pending = calculate_general_metrics(total_base, scanned_items)
    
    assert total_scanned == 3
    assert progress == 0.03 # 3%
    assert pending == 97

def test_calculate_general_metrics_full():
    total_base = 10
    scanned_items = [{'id': i} for i in range(10)]
    total_scanned, progress, pending = calculate_general_metrics(total_base, scanned_items)
    
    assert total_scanned == 10
    assert progress == 1.0
    assert pending == 0

def test_get_adjustment_items():
    scanned_items = [
        {'serial': '1', 'requires_adjustment': True},
        {'serial': '2', 'requires_adjustment': False},
        {'serial': '3', 'requires_adjustment': None},
        {'serial': '4', 'requires_adjustment': True},
    ]
    
    adjustment_items = get_adjustment_items(scanned_items)
    assert len(adjustment_items) == 2
    assert adjustment_items[0]['serial'] == '1'
    assert adjustment_items[1]['serial'] == '4'

def test_get_state_distribution():
    scanned_items = [
        {'state': 'active'},
        {'state': 'active'},
        {'state': 'stock'},
        {'state': 'broken'}
    ]
    
    distribution = get_state_distribution(scanned_items)
    
    assert isinstance(distribution, pd.Series)
    assert distribution['active'] == 2
    assert distribution['stock'] == 1
    assert distribution['broken'] == 1
    assert 'stolen' not in distribution

def test_get_state_distribution_empty():
    distribution = get_state_distribution([])
    assert distribution.empty
